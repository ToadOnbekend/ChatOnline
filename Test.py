from ClassDatabase import  DatabaseManger


databasemrg = DatabaseManger("sqlite:///MMe.db")


# k = databasemrg.get_all_users()

k = databasemrg.get_user("FD")
print(k)

# databasemrg.add_user("Toad", "Admin")

# databasemrg.create_room("main chat")
#
# databasemrg.retrive_available_rooms()
#
# databasemrg.add_message("main chat", "Toad", "Hello, here is Toad")
#
# databasemrg.retrive_available_messages_of_room("main chat")

