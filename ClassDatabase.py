from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import datetime

import pprint
pp = pprint.PrettyPrinter(indent=4)


class DatabaseManger:
    def __init__(self, database:str):
        # sqlite:///Databases/ChatMSG.db
        self.engine = create_engine(database)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        print("\033[32mCreated\033[0m")


    def retrive_available_rooms(self):
        available_rooms = {"rooms":[], "id":[], "datemade":[]}

        retrivedRooms = self.session.execute(text("""
                                        SELECT  RoomID, NameRoom, DateMade 
                                        FROM Rooms
                                        ORDER BY DateMade;
                                    """)).fetchall()

        for result in retrivedRooms:
            available_rooms["rooms"].append(result[1])
            available_rooms["id"].append(result[0])
            available_rooms["datemade"].append(result[2])


        return available_rooms

    def retrive_available_messages_of_room(self, room_name):
        available_messages = {"messageId":[],"content":[], "userName":[], "userId":[], "dateMade":[]}

        retrivedMessages = self.session.execute(text("""
                                        SELECT  Messages.MessageID, Messages.Content, Users.UserID, Users.Name, Messages.DateMade
                                        FROM Messages
                                        JOIN Users ON Users.UserID = Messages.UserID
                                        JOIN Rooms ON Rooms.RoomID = Messages.RoomID
                                        WHERE Rooms.NameRoom = :requested_room_name
                                        ORDER BY Messages.DateMade;
                                    """), {
                                    "requested_room_name":room_name
                                    }).fetchall()

        for result in retrivedMessages:
            available_messages["messageId"].append(result[0])
            available_messages["content"].append(result[1])
            available_messages["userId"].append(result[2])
            available_messages["userName"].append(result[3])

            dt = datetime.fromisoformat(result[4])
            formatted_time = dt.strftime("%H:%M")
            available_messages["dateMade"].append(formatted_time)


        pp.pprint(available_messages)
        return available_messages



    def create_room(self, name_of_room):
        date = datetime.now().isoformat()
        self.session.execute(text("""
                    INSERT INTO Rooms (NameRoom, DateMade)
                    VALUES (:NameRoomR, :DateCreated);
                """), {
            "NameRoomR": name_of_room,
            "DateCreated": date
        })
        self.session.commit()
        result_initalization_pre = self.session.execute(text("""
                                SELECT  RoomID
                                FROM Rooms
                                WHERE NameRoom = :NameRoomR
                                LIMIT 1;
                            """), {
            "NameRoomR": name_of_room
        }).fetchall()

        for result in result_initalization_pre:
            current_id = result[0]

        return current_id

    def add_user(self, name, role):

        retrivedRoleId = self.session.execute(text("""
                                                SELECT RoleID FROM Roles WHERE Status = :role ;
                                            """), {
            "role": role
        }).fetchall()

        for result in retrivedRoleId:
            current_roleID = result[0]

        date = datetime.now().isoformat()
        self.session.execute(text("""
                           INSERT INTO Users (RoleID, Name, DateMade)
                           VALUES (:roleID, :name, :dateCr );
                           
                       """), {
            "name": name,
            "roleID": current_roleID,
            "dateCr":date
        })
        self.session.commit()

    def add_message(self, room_name, user_name, content, date):
        retrivedUserId = self.session.execute(text("""
                                                       SELECT UserID  FROM Users WHERE Name = :user_name ;
                                                   """), {
            "user_name": user_name
        }).fetchall()

        for result in retrivedUserId:
            current_userID = result[0]

        retrivedRoomId = self.session.execute(text("""
                                                               SELECT RoomID  FROM Rooms WHERE NameRoom = :room_name ;
                                                           """), {
            "room_name": room_name
        }).fetchall()

        for result in retrivedRoomId:
            print(result, "Result room")
            current_RoomID = result[0]


        self.session.execute(text("""
                                  INSERT INTO Messages (RoomID, UserID, Content, DateMade)
                                  VALUES (:roomid, :userid, :content, :datemade );

                              """), {
            "roomid": current_RoomID,
            "userid": current_userID,
            "content": content,
            "datemade": date
        })
        self.session.commit()

    def get_user(self, user_name):


        retrivedUser = self.session.execute(text("""
             SELECT Name, RoleID, UserID, DateMade FROM Users 
             WHERE Name = :user_name
             LIMIT 1 ;    """), {
            "user_name": user_name
        }).fetchall()

        for result in retrivedUser:
            username = result[0]
            roleID = result[1]
            userID = result[2]
            dateMade = result[3]

        try:
          print(roleID, "\033[31m ROLE")
        except UnboundLocalError:
            return {"username": "", "roleStatus": "A", "dateMade": "No-Date-Created"}

        retrivedRoleId = self.session.execute(text("""
                 SELECT Status FROM Roles 
                 WHERE RoleID = :roleID
                 LIMIT 1 ;    """), {
                "roleID": roleID
            }).fetchall()


        for result in retrivedRoleId:
            status = result[0]

        return {"username": username, "roleStatus": status, "dateMade": dateMade}


    def get_all_users(self):
        users_col = {"Name": [], "RoleID": [], "UserID": [], "DateMade": []}
        mapping = {"1": "Admin",
                   "2": "User"}

        retrivedUser = self.session.execute(text("""
             SELECT Name, RoleID, UserID, DateMade FROM Users 
             """)).fetchall()

        for result in retrivedUser:
            users_col["Name"].append(result[0])
            users_col["RoleID"].append(mapping[str(result[1])])
            users_col["UserID"].append(result[2])
            users_col["DateMade"].append(result[3])

        return users_col



