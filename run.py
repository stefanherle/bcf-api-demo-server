from bcf_api import create_app 

app = create_app()
app.run(debug=True, use_reloader=False)