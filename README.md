#Project Description

This is the implementation of Udacity Full Stack Web Developer Nanodegree Project: Item Catalog. It is a simple CRUD operation demo using Flask framekwork and Sqlalchemy database connection. Sqlite is chosen as database for its lightweight and easy access. It also integrates 3rd party authentication using Google Sign In.

#Dependencies/Pre-requisites

Requires software and modules include:
* python 2.7.12 and above
* flask 1.0.2 and above
* sqlalchemy 1.2.16 and above
* Google api client on the server, including google.oauth2 and google.auth.transport. They can be installed by:
'''
pip install --upgrade google-api-python-client
'''

#Setup/Installation
Extract the zip file which will contain the following files:
│  application.py
│  client_secrets.json
│  database_setup.py
│  database_setup.pyc
│  itemcatalog.db
│  README.md
│  sampledb.txt
│
├─static
│      styles.css
│
└─templates
        categories.html
        categoriessection.html
        deleteCategory.html
        deleteItem.html
        editCategory.html
        editItem.html
        item.html
        itemsection.html
        login.html
        loginsection.html
        newCategory.html
        newItem.html
		
To run the project, in the main directory, execute:

'''
python application.py
'''

#Usage

To access the application from browser, use the following URL [http://localhost:5000](http://localhost:5000)

The application allow viewing for catagories and items for all users. For signed-in users, it allows CRUD update for the categories and items within them for those originally created by the same user. The authorization is associated using category as unit.

#Known Issues

None reported.

#Future Plans

Authroization model could have further consideration and a more refined model could be considered.

The authorization using category as unit is inituive and easy to work. Depends on the semantics of the actual categories and items, this might make perfect sense. Another model is to use item as unit if the semantics makes sense. In that case, category could become publicly available for CRUD operation. Authorization using combination of category/item could makes sense in some case but that model could be different to understand from user perspective.

