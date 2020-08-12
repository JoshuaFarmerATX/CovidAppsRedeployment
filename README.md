# covid-api


## Project 3

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
