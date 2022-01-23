# Certificate Manager
**About**
 - This is a sample application that allows you to create users, certificates for those users and register webhooks for updates on those certificates. There is no authorization or authentication implemented. Much of the directory structure is pulled from a [template repo](https://github.com/tiangolo/full-stack-fastapi-postgresql) created by the project maintainer. 

**Technologies**
- FastAPI. This python framework provides API documentation out of the box (visable at the `/docs` route) and supports async python. Has some cool features like [background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/), which will allow the server to respond to the request and work the remaining tasks after (still occupying the same python process though).
- PostgreSQL. An open source relational database favorite. The requirements of the project led to a simple set of data with clear relationships, making the choice straight forward. 


## Getting Started
- Clone the project repo
- From within the project directory run `docker-compose up`
	- This assumes that you have both Docker and Docker Compose installed on your machine. You can find more information [here](https://docs.docker.com/get-docker/)
- Navigate to `http://0.0.0.0:8000/docs` in your web browser.
- Can use this view to see available API routes and also create sample data. Below are some quick guides.


## Guides
All guides assume that the "Getting Started" section above is complete.

### Create a user
- On `/docs`, expand the `POST /users/` endpoint and click the "Try it out" button.
- Fill out the request body and click "Execute"
- You can see that your user id will be returned, which will be useful later on.

### Create a certificate for a user
- With your user_id in hand, expand the `POST /{user_id}/certificates` endpoint on the `/docs` page.
- Click the "Try it out" button and enter your user_id into the first field.
- We require that you provide your certificate an "alias" just to keep things organized from a UX perspective, so you can keep your many certificates organized.
- After adding the alias to the request body click "Execute".
- You can see that your certificate id will be returned, which can be useful later on.

### Register a webhook for a certificate
- With your user_id and certificate_id in hand, expand the `POST /{user_id}/certificates/{certificate_id}` endpoint on the `/docs` page.
- Click the "Try it out" button and enter your user_id and certificate_id into the required fields.
- Add a url into the request body and click "Execute".

### Make an update to your certificate and trigger a webhook
- After you have created a user, associated a certificate with that user, and assoicated a webhook with that certificate, you're ready to test an update!
- Expand the `PUT /{user_id}/certificates/{certificate_id}` section of the `/docs` page.
- Click "Try it out" then enter the required user_id and certificate_id fields.
- After you can see that you can only update the "active" or "alias" properties of an existing certificate.
- Make an update to both or one of "active" and "alias" then click execute.
- You will see your response and can go to your webhook URL desitnation to see that we submitted a `POST` request with all the certificate data (except `private_key`)
