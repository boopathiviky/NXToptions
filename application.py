#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import timedelta

from flask import Flask
from api.conf.config import es
from api.routes.user_routes import generate_routes
from api.handlers_user.schema import genrate_token, mailapp
from flask_jwt_extended import JWTManager
from flask_mail import Mail

application = Flask(__name__)

# Set debug true for catching the errors.
application.config['DEBUG'] = True
application.config["JWT_SECRET_KEY"] = "jbi434bhb34uui3o34383rbu3b34ggygygugugugyugugu"  # Change this!
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
application.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
application.config['MAIL_SERVER']='smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'lingeshw536@gmail.com'
application.config['MAIL_PASSWORD'] = 'viky@13752410'
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
mail = Mail(application)
jwt = JWTManager(application)
mailapp(mail)
genrate_token(jwt)


# check all index exists
# lst=["profiledetails","debit","credit"]
# if es.indices.exists(index="profiledetails") == False:
#     for ind in range(len(lst)):
#         print(es.indices.create(index=ind))
# Generate routes.
generate_routes(application)




if __name__ == '__main__':
    # Run app. For production use another web server.
    # Set debug and use_reloader parameters as False.
    application.debug = True
    application.run()
