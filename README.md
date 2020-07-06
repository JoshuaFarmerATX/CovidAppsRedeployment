# Use our Sites!
API: https://api-app-pjblaypjta-uc.a.run.app/docs
Project 2: https://app-sr6kth3fza-uc.a.run.app/
Project 3: https://front-facing-pjblaypjta-uc.a.run.app/

# Redeployment Manual

## Getting started on GCP

1. Make sure you have the SDK installed on your computer.
2. Go to console.cloud.google.com
3. Create two projects and name them anything you like (perhaps Project 2 and Project 3)
4. Open the "Cloud Run" app and enable it
5. Open the "Cloud SQL" app and enable it
6. Open the "App Engine" app and enable it (if it isn't already)
6. Clone the redeployment repo

## Project 2
### Before you start: be sure you are on the Project 2 project (or whatever you called it) at console.cloud.google.com.

#### 1. Go to console.cloud.google.com and open the Cloud SQL app
#### 2. Create a new Cloud SQL instance
1. Create a MySQL instance
2. Use whatever you like for the instance ID
3. Set the root password to "ehaarmanny"
4. Use MySQL 5.6 for the database version
5. Everything else can be left to default.
#### 3. Copy the instance connection name into another document to use later.
#### 4. Once the instance initializes, go into the instance, click "Databases" and create a database named "Covid" (capitalization matters)
#### 5. In the project 2 repo folder, open Bash and type "gcloud init." Point the Google Cloud SDK to your Project 2 project
#### 6. In the Data Loader folder
1. Open app.py
    * At line 120, change the string "project2-270717:us-central1:covid2019" to match your project ID/database instance connection name
2. Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/dataloader:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
3. On Google Cloud Console, open the Google Cloud Run app. 
    1. Click "Create Service" at the top
    2. Call the service whatever you like.
    3. Click "allow unauthenticated invocations"
    4. Click "next"
    5. Click "select" on the container image URL. Click the latest container under "dataloader"
    6. Click "show advanced settings"
    7. Set the memory allocation to 2 gi2.
    8. Scroll back to where the "show advanced settings" button was and click "Connections"
    9. Under "Cloud SQL connections" click "add connection."
    10. Connect to the Cloud SQL instance you created above.
    11. Click "create" at the bottom.
    12. After the app deploys, click the app link to ensure it works. The loader will run and it may take a minute or two to complete.
#### 7. In the App folder, go into the app folder.
1. Open plot.py
    1. At line 12, change the string "project2-270717:us-central1:covid2019" to match your project ID/database instance connection name
2. Open database.py
    1. At line 17, change the string "project2-270717:us-central1:covid2019" to match your project ID/database instance connection name
3. Open map_plots.py
    1. At line 10, change the string "project2-270717:us-central1:covid2019" to match your project ID/database instance connection name
4. Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/app:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
5. On Google Cloud Console, open the Google Cloud Run app. 
    1. Click "Create Service" at the top
    2. Call the service whatever you like.
    3. Click "allow unauthenticated invocations"
    4. Click "next"
    5. Click "select" on the container image URL. Click the latest container under "appr"
    6. Click "show advanced settings"
    7. Set the memory allocation to 2 gi2.
    8. Scroll back to where the "show advanced settings" button was and click "Connections"
    9. Under "Cloud SQL connections" click "add connection."
    10. Connect to the Cloud SQL instance you created above.
    11. Click "create" at the bottom.
    12. After the app deploys, click the app link to ensure it works.
6. After you have completed the steps for Project 3, open templates/layout.html
    1. Update the API link at Line 23
    2. Follow the instructions at letter d
    3. On Google Cloud Console, go into Google Cloud Run, click the service serving the Project 2 app, and click "Deploy New Revision at the top"
    4. Point the new revision to the latest app container. You need do nothing else but deploy the revision.
#### 8. Double check HTML files to ensure all links were updated.
#### 9. If you get an error or need to deploy one of the apps, follow the instructions at 7.5 to deploy a new revision, using the appropriate container name at step 7.5.ii.

## Project 3
### Before you start: be sure you are on the Project 3 project (or whatever you called it) at console.cloud.google.com.

Project 3 will, because of its modularization, be far easier to redeploy.

#### 1. Go to console.cloud.google.com and open the Cloud SQL app
#### 2. Create a new Cloud SQL instance
1. Create a MySQL instance
2. Use whatever you like for the instance ID
3. Set the root password to "ehaarmanny"
4. Use MySQL 5.6 for the database version
5. Everything else can be left to default.
#### 3. Copy the instance connection name into another document to use later.
#### 4. Once the instance initializes, go into the instance, click "Databases" and create a database named "Covid" (capitalization matters)
#### 5. In the project 3 repo folder, open Bash and type "gcloud init." Point the Google Cloud SDK to your Project 3 project.
#### 6. In the Global Daily Cases Dataloader folder
1. Open connection.py
    1. In conn_string_deploy, change the string "covid-api-274519:us-central1:covid-19" to match your project ID/database instance connection name
2. Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/globalcasesloader:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
3. On Google Cloud Console, open the Google Cloud Run app. 
    1. Click "Create Service" at the top
    2. Call the service whatever you like.
    3. Click "allow unauthenticated invocations"
    4. Click "next"
    5. Click "select" on the container image URL. Click the latest container under "globalcasesloader"
    6. Click "show advanced settings"
    7. Set the memory allocation to 2 gi2.
    8. Scroll back to where the "show advanced settings" button was and click "Connections"
    9. Under "Cloud SQL connections" click "add connection."
    10. Connect to the Cloud SQL instance you created above.
    11. Click "create" at the bottom.
    12. After the app deploys, click the app link to ensure it works. The loader will run and it may take a minute or two to complete.
#### 7. In the USA Dataloader folder
1. Open connection.py
    1. In conn_string_deploy, change the string "covid-api-274519:us-central1:covid-19" to match your project ID/database instance connection name
2. Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/usaloader:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
3. On Google Cloud Console, open the Google Cloud Run app. 
    1. Click "Create Service" at the top
    2. Call the service whatever you like.
    3. Click "allow unauthenticated invocations"
    4. Click "next"
    5. Click "select" on the container image URL. Click the latest container under "usaloader"
    6. Click "show advanced settings"
    7. Set the memory allocation to 2 gi2.
    8. Scroll back to where the "show advanced settings" button was and click "Connections"
    9. Under "Cloud SQL connections" click "add connection."
    10. Connect to the Cloud SQL instance you created above.
    11. Click "create" at the bottom.
    12. After the app deploys, click the app link to ensure it works. The loader will run and it may take a minute or two to complete.
#### 8. In the API App Folder
1. Open connection.py
    1. In conn_string_deploy, change the string "covid-api-274519:us-central1:covid-19" to match your project ID/database instance connection name
2. Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/api:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
3. On Google Cloud Console, open the Google Cloud Run app. 
    1. Click "Create Service" at the top
    2. Call the service whatever you like.
    3. Click "allow unauthenticated invocations"
    4. Click "next"
    5. Click "select" on the container image URL. Click the latest container under "api"
    6. Click "show advanced settings"
    7. Set the memory allocation to 2 gi2.
    8. Scroll back to where the "show advanced settings" button was and click "Connections"
    9. Under "Cloud SQL connections" click "add connection."
    10. Connect to the Cloud SQL instance you created above.
    11. Click "create" at the bottom.
    12. After the app deploys, click the app link to ensure it works. Add /docs onto the link to get to the actual API.
#### 9. In the Modeler Folder
1. Open app.py
    1. Change line 17 to reflect the new API link
2. Open modeling.py
    1. Change line 12 to reflect the new API link
3. Open modeling_us.py
    1. Change lines 19 and 32 to reflect the new API link
4. Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/modeling:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
5. On Google Cloud Console, open the Google Cloud Run app. 
    1. Click "Create Service" at the top
    2. Call the service whatever you like.
    3. Click "allow unauthenticated invocations"
    4. Click "next"
    5. Click "select" on the container image URL. Click the latest container under "modeling"
    6. Click "show advanced settings"
    7. Set the memory allocation to 2 gi2.
    8. Scroll back to where the "show advanced settings" button was and click "Connections"
    9. Under "Cloud SQL connections" click "add connection."
    10. Connect to the Cloud SQL instance you created above.
    11. Click "create" at the bottom.
    12. After the app deploys, click the app link to ensure it works. You'll get a message that says "Working" if it is.
#### 10. In the Streamlit folder
1. Open app.py
    1. Change lines 25 and 28 to reflect the new API link
    2. Change lines 35 and 38 to reflect the new modeler link
2. Open Bash and type "gcloud app deploy"
3. After the app deploys, click the app link to ensure it works.
#### 11. In the "Front facing" folder
1. Open covidSource.py
    1. Update the API link at lines 7, 19, and 42
2. Open templates/index.html
    1. Update the Streamlit app link at line 42
3. Open templates/layout.html
    1. Update the Streamlit app link at line 42
4. Open templates/layout.html
    1. Update the Covid Data Site URL at line 20 and 42 to your Project 2 link.
    2. Update the API link at line 60
4. Open Bash and type "gcloud builds submit --tag gcr.io/covid-api-274519/frontfacing:latest" where covid-api-274519 is replaced with your Project ID (found at console.cloud.google.com under "Project Info")
5. On Google Cloud Console, open the Google Cloud Run app. 
    1. Click "Create Service" at the top
    2. Call the service whatever you like.
    3. Click "allow unauthenticated invocations"
    4. Click "next"
    5. Click "select" on the container image URL. Click the latest container under "frontfacing"
    6. Click "show advanced settings"
    7. Set the memory allocation to 2 gi2.
    8. Scroll back to where the "show advanced settings" button was and click "Connections"
    9. Under "Cloud SQL connections" click "add connection."
    10. Connect to the Cloud SQL instance you created above.
    11. Click "create" at the bottom.
    12. After the app deploys, click the app link to ensure it works. The loader will run and it may take a minute or two to complete.
#### 12. Double check HTML files to ensure all links were updated.
#### 13. If you get an error or need to deploy one of the apps, follow the instructions at 6.3 to deploy a new revision, using the appropriate container name at step 6.3.ii.
