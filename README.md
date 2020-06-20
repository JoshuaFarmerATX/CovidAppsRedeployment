# Redeployment Manual

## Getting started on GCP

1) Make sure you have the SDK installed on your computer.
2) Go to console.cloud.google.com
3) Create two projects and name them anything you like (perhaps Project 2 and Project 3)
4) Open the "Cloud Run" app and enable it
5) Open the "Cloud SQL" app and enable it
6) Open the "App Engine" app and enable it (if it isn't already)
6) Clone the redeployment repo

## Project 2
### Before you start: be sure you are on the Project 2 project (or whatever you called it) at console.cloud.google.com.

1) Go to console.cloud.google.com and open the Cloud SQL app
2) Create a new Cloud SQL instance
    a) Create a MySQL instance
    b) Use whatever you like for the instance ID
    c) Set the root password to "ehaarmanny"
    d) Use MySQL 5.6 for the database version
    e) Everything else can be left to default.
3) Copy the instance connection name into another document to use later.
4) Once the instance initializes, go into the instance, click "Databases" and create a database named "Covid" (capitalization matters)
5) In the project 2 repo folder, open Bash and type "gcloud init." Point the Google Cloud SDK to your Project 2 project.
5) In the Data Loader folder
    a) Open app.py
        i) At line 120, change the string "project2-270717:us-central1:covid2019" to match your project ID/database instance connection name
    b) Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/dataloader:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
    c) On Google Cloud Console, open the Google Cloud Run app. 
        i) Click "Create Service" at the top
        ii) Call the service whatever you like.
        iii) Click "allow unauthenticated invocations"
        iv) Click "next"
        v) Click "select" on the container image URL. Click the latest container under "dataloader"
        vi) Click "show advanced settings"
        vii) Set the memory allocation to 2 gib.
        viii) Scroll back to where the "show advanced settings" button was and click "Connections"
        ix) Under "Cloud SQL connections" click "add connection."
        x) Connect to the Cloud SQL instance you created above.
        xi) Click "create" at the bottom.
        xii) After the app deploys, click the app link to ensure it works. The loader will run and it may take a minute or two to complete.
6) In the App folder, go into the app folder.
    a) Open plot.py
        i) At line 12, change the string "project2-270717:us-central1:covid2019" to match your project ID/database instance connection name
    b) Open database.py
        i) At line 17, change the string "project2-270717:us-central1:covid2019" to match your project ID/database instance connection name
    c) Open map_plots.py
        i) At line 10, change the string "project2-270717:us-central1:covid2019" to match your project ID/database instance connection name
    d) Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/app:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
    e) On Google Cloud Console, open the Google Cloud Run app. 
        i) Click "Create Service" at the top
        ii) Call the service whatever you like.
        iii) Click "allow unauthenticated invocations"
        iv) Click "next"
        v) Click "select" on the container image URL. Click the latest container under "appr"
        vi) Click "show advanced settings"
        vii) Set the memory allocation to 2 gib.
        viii) Scroll back to where the "show advanced settings" button was and click "Connections"
        ix) Under "Cloud SQL connections" click "add connection."
        x) Connect to the Cloud SQL instance you created above.
        xi) Click "create" at the bottom.
        xii) After the app deploys, click the app link to ensure it works.
    f) After you have completed the steps for Project 3, open templates/layout.html
        i) Update the API link at Line 23
        ii) Follow the instructions at letter d
        iii) On Google Cloud Console, go into Google Cloud Run, click the service serving the Project 2 app, and click "Deploy New Revision at the top"
        iv) Point the new revision to the latest app container. You need do nothing else but deploy the revision.
7) Double check HTML files to ensure all links were updated.
8) If you get an error or need to deploy one of the apps, follow the instructions at 7(f) to deploy a new revision, using the appropriate container name at step 7(f)(ii).

## Project 3
### Before you start: be sure you are on the Project 3 project (or whatever you called it) at console.cloud.google.com.

Project 3 will, because of its modularization, be far easier to redeploy.

1) Go to console.cloud.google.com and open the Cloud SQL app
2) Create a new Cloud SQL instance
    a) Create a MySQL instance
    b) Use whatever you like for the instance ID
    c) Set the root password to "ehaarmanny"
    d) Use MySQL 5.6 for the database version
    e) Everything else can be left to default.
3) Copy the instance connection name into another document to use later.
4) Once the instance initializes, go into the instance, click "Databases" and create a database named "Covid" (capitalization matters)
5) In the project 3 repo folder, open Bash and type "gcloud init." Point the Google Cloud SDK to your Project 3 project.
5) In the Global Daily Cases Dataloader folder
    a) Open connection.py
        i) In conn_string_deploy, change the string "covid-api-274519:us-central1:covid-19" to match your project ID/database instance connection name
    b) Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/globalcasesloader:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
    c) On Google Cloud Console, open the Google Cloud Run app. 
        i) Click "Create Service" at the top
        ii) Call the service whatever you like.
        iii) Click "allow unauthenticated invocations"
        iv) Click "next"
        v) Click "select" on the container image URL. Click the latest container under "globalcasesloader"
        vi) Click "show advanced settings"
        vii) Set the memory allocation to 2 gib.
        viii) Scroll back to where the "show advanced settings" button was and click "Connections"
        ix) Under "Cloud SQL connections" click "add connection."
        x) Connect to the Cloud SQL instance you created above.
        xi) Click "create" at the bottom.
        xii) After the app deploys, click the app link to ensure it works. The loader will run and it may take a minute or two to complete.
6) In the USA Dataloader folder
    a) Open connection.py
        i) In conn_string_deploy, change the string "covid-api-274519:us-central1:covid-19" to match your project ID/database instance connection name
    b) Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/usaloader:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
    c) On Google Cloud Console, open the Google Cloud Run app. 
        i) Click "Create Service" at the top
        ii) Call the service whatever you like.
        iii) Click "allow unauthenticated invocations"
        iv) Click "next"
        v) Click "select" on the container image URL. Click the latest container under "usaloader"
        vi) Click "show advanced settings"
        vii) Set the memory allocation to 2 gib.
        viii) Scroll back to where the "show advanced settings" button was and click "Connections"
        ix) Under "Cloud SQL connections" click "add connection."
        x) Connect to the Cloud SQL instance you created above.
        xi) Click "create" at the bottom.
        xii) After the app deploys, click the app link to ensure it works. The loader will run and it may take a minute or two to complete.
7) In the API App Folder
    a) Open connection.py
        i) In conn_string_deploy, change the string "covid-api-274519:us-central1:covid-19" to match your project ID/database instance connection name
    b) Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/api:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
    c) On Google Cloud Console, open the Google Cloud Run app. 
        i) Click "Create Service" at the top
        ii) Call the service whatever you like.
        iii) Click "allow unauthenticated invocations"
        iv) Click "next"
        v) Click "select" on the container image URL. Click the latest container under "api"
        vi) Click "show advanced settings"
        vii) Set the memory allocation to 2 gib.
        viii) Scroll back to where the "show advanced settings" button was and click "Connections"
        ix) Under "Cloud SQL connections" click "add connection."
        x) Connect to the Cloud SQL instance you created above.
        xi) Click "create" at the bottom.
        xii) After the app deploys, click the app link to ensure it works. Add /docs onto the link to get to the actual API.
8) In the Modeler Folder
    a) Open app.py
        i) Change line 17 to reflect the new API link
    b) Open modeling.py
        i) Change line 12 to reflect the new API link
    c) Open modeling_us.py
        i) Change lines 19 and 32 to reflect the new API link
    d) Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/modeling:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
    e) On Google Cloud Console, open the Google Cloud Run app. 
        i) Click "Create Service" at the top
        ii) Call the service whatever you like.
        iii) Click "allow unauthenticated invocations"
        iv) Click "next"
        v) Click "select" on the container image URL. Click the latest container under "modeling"
        vi) Click "show advanced settings"
        vii) Set the memory allocation to 2 gib.
        viii) Scroll back to where the "show advanced settings" button was and click "Connections"
        ix) Under "Cloud SQL connections" click "add connection."
        x) Connect to the Cloud SQL instance you created above.
        xi) Click "create" at the bottom.
        xii) After the app deploys, click the app link to ensure it works. You'll get a message that says "Working" if it is.
9) In the Streamlit folder
    a) Open app.py
        i) Change lines 25 and 28 to reflect the new API link
        ii) Change lines 35 and 38 to reflect the new modeler link
    b) Open Bash and type "gcloud app deploy"
    c) After the app deploys, click the app link to ensure it works.
10) In the "Front facing" folder
    a) Open covidSource.py
        i) Update the API link at lines 7, 19, and 42
    b) Open templates/index.html
        i) Update the Streamlit app link at line 42
    c) Open templates/layout.html
        i) Update the Streamlit app link at line 42
    d) Open templates/layout.html
        i) Update the Covid Data Site URL at line 20 and 42 to your Project 2 link.
        ii) Update the API link at line 60
    d) Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/frontfacing:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
    e) On Google Cloud Console, open the Google Cloud Run app. 
        i) Click "Create Service" at the top
        ii) Call the service whatever you like.
        iii) Click "allow unauthenticated invocations"
        iv) Click "next"
        v) Click "select" on the container image URL. Click the latest container under "frontfacing"
        vi) Click "show advanced settings"
        vii) Set the memory allocation to 2 gib.
        viii) Scroll back to where the "show advanced settings" button was and click "Connections"
        ix) Under "Cloud SQL connections" click "add connection."
        x) Connect to the Cloud SQL instance you created above.
        xi) Click "create" at the bottom.
        xii) After the app deploys, click the app link to ensure it works. The loader will run and it may take a minute or two to complete.
11) Double check HTML files to ensure all links were updated.
12) If you get an error or need to deploy one of the apps, follow the instructions at 7(f) to deploy a new revision, using the appropriate container name at step 7(f)(ii).
