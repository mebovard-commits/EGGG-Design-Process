from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("EGG Design Process")
set_website_framed(False)

set_site_information(
    author='Madeline Bovard',
    description='This website is supposed to help EGGG students work through design processes',
    sources=[],
    planning=[
        "Copy of CS1 Final Project 1: Design",
        "Copy of CS1 Final Project 0: Pick a Problem"
    ],
    links=[]
)
@dataclass
class DesignTask:
    task_title: str
    task_description: str
    task_layer: str
    completed: bool

@dataclass
class State:
    project_name: str
    project_goal: str
    task: list[DesignTask]
    notes: list[str]
    

@route
def index(state: State)-> Page:
    return Page(state,[
        Header("Engineering Design Organizer"),
        Text("Welcome to Your Design Organizer!"),
        Button("My Project", project_input_page),
        Button("View Tasks", tasks_page),
        Button("View Notes", notes_page),
        Button("Design Layers", layers_page)
    ])
@route
def tasks_page(state: State) -> Page:
    content = [
        Header("My Project Tasks"),
        Button("Add New Task", task_input_page)
        ]
    for index, task in enumerate(state.task):
        content.append(Header(task.task_title))
        content.append(Text(task.task_description))
        content.append(Text("Layer: " + task.task_layer))
        
        if task.completed:
            content.append(Text("Completed"))
        else:
            content.append(Text("Not Completed"))
            content.append(Button("Mark Complete",
                                  complete_task,
                                  task_index=index))
            
    return Page(state, content)
    
@route
def add_task(state: State, title: str, description: str, layer: str)-> Page:
    if title != "":
        new_task = DesignTask(
            title,
            description,
            layer,
            False
        )
        state.task.append(new_task)
        
    return tasks_page(state)

@route
def complete_task(state: State, task_index: int) -> Page:
    state.task[task_index].completed = True
    return tasks_page(state)

@route
def add_note(state: State, note: str)-> Page:
    if note != "":
        state.notes.append(note)
    return notes_page(state)

@route
def project_page(state: State)-> Page:
    return Page(state, [
        Header("My Project"),
        Text("Project Name: " + state.project_name),
        Text("Project Goal: " + state.project_goal),
        Button("Edit project", project_input_page),
        Button("Home", index)
    ])

@route
def project_input_page(state: State)-> Page:
    return Page(state, [
        Header("Set Up Your Project"),
        Text("Enter Your project Information Below"),
        TextBox("project_name", "Project Name"),
        TextArea("project_goal", "Project Goal"),
        Button("Save project", save_project)
    ])

@route
def save_project(state: State, project_name: str, project_goal: str) -> Page:
    state.project_name = project_name
    state.project_goal = project_goal
    return project_page(state)
                     

@route
def layers_page(state: State)-> Page:
    return Page(state, [
        Header("Design process Layers"),
        Text("1. Identify Problem"),
        Text("2. Research"),
        Text("3. Design"),
        Text("4. prototype"),
        Text("5. Evaluate"),
        Button("Home", index)
    ])

@route
def notes_page(state:State) ->Page:
    content = [
        Header("My Project Notes"),
        Button("Add New Note", note_input_page)
    ]
    for note in state.notes:
        content.append(Text(note))
    content.append(Button("Home", index))
    return Page(state, content)

@route
def task_input_page(state: State) -> Page:
    return Page(state, [
        Header("Add a New Task"),
        TextBox("Task title", "title"),
        TextArea("Task Description", "description"),
        SelectBox("Design Layer",
                  ["Identify Problem", "Research",
                   "Design", "prototype",
                   "Evaluate"],
                  "layer"),
        Button("Save Task", add_task)
    ])

@route
def note_input_page(state: State) -> Page:
    return Page(state, [
        Header("Add a Note"),
        TextArea("Enter_Your_Note", "note"),
        Button("Save Note", add_note)
    ])

initial_state = State(
    project_name = "",
    project_goal = "",
    task = [],
    notes = []
)

start_server(initial_state)
    
    
