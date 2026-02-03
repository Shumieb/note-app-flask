from flask import Flask, request, render_template

app = Flask(__name__)


next_id = 5

notes = [
    {"id":"1", "note":"This is note number 1", "priority":"high", "complete": False},
    {"id":"2", "note":"This is note number 2", "priority":"low", "complete": False},
    {"id":"3", "note":"This is note number 3", "priority":"medium", "complete": False},
    {"id":"4", "note":"This is note number 4", "priority":"medium", "complete": True},
]

## render html templates

# render home page
@app.route("/")
def home_page():
    return render_template("index.html", notes=notes)

@app.route("/add-note")
def show_add_note_page():
    return render_template("add-note.html")

@app.route("/edit-note/<id>")
def show_edit_note_page(id):
    return render_template("edit-note.html", note_id=id)

@app.route("/delete-note/<id>")
def show_delete_note_page(id):
    return render_template("delete-note.html", note_id=id)

# render about page
@app.route("/about")
def about_page():
    return render_template("about.html")

# render contact page
@app.route("/contact")
def contact_page():
    return render_template("contact.html")


## interact with data

# list all notes
@app.get("/notes")
def list_notes():
    return notes


# list a single note
@app.get("/notes/<id>")
def list_single_note(id):
    for note in notes:
        if note["id"] == id:
            return note
    
    return f"Note with id {id} not found"


# add new note
@app.post("/notes")
def create_note():
    global next_id

    if len(request.json["note"]) < 3:
        return "Please enter a note"

    new_note = {
        "id": f'{next_id}',
        "note": request.json["note"],
        "priority": request.json["priority"] if "priority" in request.json else "low",
        "complete": False
    }

    next_id += 1

    notes.append(new_note)

    return new_note


# update a note
@app.put("/notes/<id>")
def update_note(id):
    for note in notes:
        if note["id"] == id:
            note["note"] = request.json["note"] if "note" in request.json else note["note"]
            note["priority"] = request.json["priority"] if "priority" in request.json else note["priority"]
            note["complete"] = request.json["complete"] if "complete" in request.json else note["complete"]
            return note
    
    return f"Note with id {id} not found"


# delete a note
@app.delete("/notes/<id>")
def delete_note(id):
    for note in notes:
        if note["id"] == id:
            notes.remove(note)
            return note
    
    return f"Note with id {id} not found"


# get notes by priority
@app.get("/notes/priority/<priority>")
def notes_by_priority(priority):
    filtered_notes = [note for note in notes if note["priority"] == priority]
    
    if len(filtered_notes) > 0:
        return filtered_notes
    
    return f"No notes with the priority - {priority} - to return"



app.run()