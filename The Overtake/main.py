from ursina import * 

app=Ursina()





def input(key):
    if key == "escape":
        quit()

if __name__ == "__main__":
    app.run()