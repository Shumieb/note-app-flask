from flask import Flask, request, render_template, redirect

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
    for note in notes:
        if note["id"] == f'{id}':
            return render_template("edit-note.html", note=note)
        
    return render_template("edit-note.html", note=id)


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
# update a note
@app.post("/notes", defaults={'id': None})
@app.post("/notes/<id>")
def create_note(id):
    global next_id

    if id is None:
        if len(request.form.get("note_desc")) > 3:
            new_note = {
                "id": f'{next_id}',
                "note": request.form.get("note_desc"),
                "priority": request.form.get("priority"),
                "complete": False
            }

            next_id += 1

            notes.append(new_note)

    else:
        for note in notes:
            if note["id"] == id:
                note["note"] = request.form.get("note_desc") 
                note["priority"] = request.form.get("priority")

    return render_template("index.html", notes=notes)


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