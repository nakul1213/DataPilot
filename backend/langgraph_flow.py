from agents.planner_agent import PlannerAgent
from agents.code_writer_agent import CodeWriterAgent
from agents.verifier_agent import VerifierAgent
from agents.output_generator import OutputGenerator

from typing import List, Dict
import os
import time
import pandas as pd

 
try:
    from langgraph.graph import StateGraph, END, START
except ImportError:
    StateGraph = None  # For type checking if not installed
    END = None
    START = None

# Define the state that will be passed between nodes
class AgentState(dict):
    """
    State dict for passing information between agents. 

    csv_path: str
    tasks: List[str]
    code_blocks: List[str]
    current_task_idx: int
    verification: dict
    summary: str
    notebook_path: str
    current_code: str
    current_task: str
    done: bool
    error: str
    feedback: str
    success: bool
    step_count: int
    failure_count: int  # Number of consecutive failures for the current task
    skipped_tasks: List[str]  # List of skipped tasks due to repeated failures
    csv_schema: str
    csv_sample: dict
    """
    csv_path: str
    tasks: List[str]
    code_blocks: List[str]
    current_task_idx: int
    verification: dict
    summary: str
    notebook_path: str
    current_code: str
    current_task: str
    done: bool
    error: str
    feedback: str
    success: bool
    current_task_idx: int
    step_count: int
    failure_count: int
    skipped_tasks: List[str]
    csv_schema: str
    csv_sample: dict

    

# Node: Planner Agent
def planner_node(state: AgentState) -> AgentState:
    
    planner = PlannerAgent(state['csv_path'])
    tasks = planner.generate_tasks()
    state['tasks'] = tasks
    state['code_blocks'] = []
    state['current_task_idx'] = 0
    # Add schema and sample to state for downstream use
    df = pd.read_csv(state['csv_path'])
    state['csv_schema'] = str(df.dtypes)
    state['csv_sample'] = df.head(3).to_dict()
     
    return state

# Node: Code Writer Agent
def code_writer_node(state: AgentState) -> AgentState:
     
    idx = state['current_task_idx']
    task = state['tasks'][idx]
    code_writer = CodeWriterAgent()
    # Pass schema and sample as context
    context = {
        'csv_schema': state.get('csv_schema', ''),
        'csv_sample': state.get('csv_sample', {})
    }
    code = code_writer.write_code(task, context=context)
    state['current_code'] = code
    state['current_task'] = task
     
    return state

# Node: Verifier Agent
def verifier_node(state: AgentState) -> AgentState:
    verifier = VerifierAgent()
    code = state['current_code']
    result = verifier.verify_code(code)
    state['verification'] = result
    return state

# Node: Output Generator
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def output_generator_node(state: AgentState) -> AgentState:
    
    output_gen = OutputGenerator()
    notebook_path = os.path.join(OUTPUT_DIR, 'pipeline.ipynb')
    readme_path = os.path.join(OUTPUT_DIR, 'README.md')
    output_gen.create_notebook(state['code_blocks'], notebook_path)
    summary = f"Tasks performed: {', '.join(state['tasks'])}"
    output_gen.create_readme(summary, readme_path)
    state['notebook_path'] = notebook_path
    state['readme_path'] = readme_path
    state['summary'] = summary
     
    return state

# Conditional transition after verifier

def verifier_router(state: AgentState) -> str:
    if state['verification']['success']:
        return 'success'
    else:
        return 'failure'

# Node: On success, append code and move to next task or finish

def on_success_node(state: AgentState) -> AgentState:
   
    state['code_blocks'].append(state['current_code'])
    state['current_task_idx'] += 1
    if state['current_task_idx'] >= len(state['tasks']):
        state['done'] = True
         
    else:
        state['done'] = False
        
    return state

# Node: On failure, retry or skip task

def on_failure_node(state: AgentState) -> AgentState:
    
    if 'failure_count' not in state:
        state['failure_count'] = 0
    state['failure_count'] += 1
    feedback = state.get('verification', {}).get('feedback', '')
    state['feedback'] = feedback
    if state['failure_count'] > 3:
        if 'skipped_tasks' not in state:
            state['skipped_tasks'] = []
        state['skipped_tasks'].append(state.get('current_task', 'Unknown Task'))
        state['code_blocks'].append(f"# Skipped task: {state.get('current_task', 'Unknown Task')} due to repeated failures.\n# Feedback: {feedback}")
        state['current_task_idx'] += 1
        state['failure_count'] = 0
        if state['current_task_idx'] >= len(state['tasks']):
            state['done'] = True
           
        else:
            state['done'] = False
            
    else:
        state['done'] = False
       
    return state

# Main workflow definition

def run_pipeline(csv_path: str, max_steps: int = 30) -> Dict:
    if StateGraph is None:
        raise ImportError("LangGraph is not installed.")
    workflow = StateGraph(AgentState)
    workflow.add_node('planner', planner_node)
    workflow.add_node('code_writer', code_writer_node)
    workflow.add_node('verifier', verifier_node)
    workflow.add_node('on_success', on_success_node)
    workflow.add_node('on_failure', on_failure_node)
    workflow.add_node('output_generator', output_generator_node)

    # Edges
    workflow.add_edge(START, 'planner')
    workflow.add_edge('planner', 'code_writer')
    workflow.add_edge('code_writer', 'verifier')
    workflow.add_conditional_edges('verifier', verifier_router, {'success': 'on_success', 'failure': 'on_failure'})
    workflow.add_edge('on_failure', 'code_writer')  # Retry same task
    def success_router(state: AgentState) -> str:
        return 'output_generator' if state.get('done') else 'code_writer'
    workflow.add_conditional_edges('on_success', success_router, {'output_generator': 'output_generator', 'code_writer': 'code_writer'})
    workflow.add_edge('output_generator', END)

    graph = workflow.compile()
    # Initial state
    state = AgentState({'csv_path': csv_path, 'step_count': 0})
    try:
        for _ in range(max_steps):
            result = graph.invoke(state)
            if result.get('notebook_path') or result.get('notebook'):
                return {
                    "notebook": f"outputs/pipeline.ipynb",
                    "readme": f"outputs/README.md",
                    "summary": result.get("summary", ""),
                }
            state['step_count'] = state.get('step_count', 0) + 1
        return {
            "notebook": "",
            "readme": "",
            "summary": f"Pipeline stopped: exceeded max_steps ({max_steps}) to prevent infinite loop.",
            "error": "Max steps exceeded."
        }
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"Error during pipeline execution: {error_msg}")
        return {
            "notebook": "",
            "readme": "",
            "summary": f'Pipeline failed with error: {str(e)}',
            "error": error_msg
        } 