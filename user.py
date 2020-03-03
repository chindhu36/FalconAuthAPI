import falcon, json, os
from sqlalchemy.orm import sessionmaker
from employee_app_falcon_token.dbconfig import engine
from employee_app_falcon_token.models import User_model as User

token=""

class User_class(object):
    def __init__(self):
        Session=sessionmaker(bind=engine)
        self.session=Session()

    def on_put(self,req,resp):
        user=self.session.query(User).all()
        if user:
            doc="User already exists"
            resp.body=json.dumps(doc)
            resp.status=falcon.HTTP_OK
        else:
            data=req.media
            if not data:
                resp.body=json.dumps("No data")
                resp.status=falcon.HTTP_OK
            else:
                un=data['username']
                user=User(user_name=un)
                user.set_password(data['password'])
                self.session.add(user)
                self.session.commit()
                self.session.close()
                doc='User added'
                resp.body=json.dumps(doc)
                resp.status=falcon.HTTP_OK

    def on_get(self,req,resp):
        data=req.media
        if not data:
            resp.body=json.dumps("No data")
            resp.status=falcon.HTTP_OK
        else:
            user=self.session.query(User).get(1)
            if user and user.check_password(data['password']):
                token=user.get_token()
                self.session.commit()
                self.session.close()
                doc={"token":token}
                resp.body=json.dumps(doc)
                resp.status=falcon.HTTP_OK
            else:
                doc="Invalid user"
                resp.body=json.dumps(doc)
                resp.status=falcon.HTTP_OK
