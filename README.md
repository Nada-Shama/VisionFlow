\# VisionFlow



\## Description

VisionFlow is a web-based platform designed to showcase creative works in graphic design, interior design, and digital drawing. It allows users to upload designs, like, and comment on them, fostering a community of creativity and inspiration.



\## Features

\- Upload designs in various categories.

\- Like and comment on designs.

\- View designs by category.

\- User profile management with profile pictures.

\- Responsive and modern UI.



\## Installation Instructions

Follow these steps to set up VisionFlow locally:



1\. Clone the repository:

&nbsp;  git clone https://github.com/nada-shamaa/visionflow.git



2\. Go into the project folder:

&nbsp;  cd visionflow



3\. Apply migrations:

&nbsp;  python manage.py migrate



4\. Run the server:

&nbsp;  python manage.py runserver



\## Usage

Once the server is running, you can:

\- Visit http://127.0.0.1:8000/ to explore the site.

\- Register a user account to upload your designs.

\- Browse designs by category: Graphic Design, Interior Design, Digital Drawing.

\- Like and comment on other users’ designs in real time.

\- Manage your profile, including uploading a profile picture.

\- Enjoy a responsive, user-friendly interface.



\## Technologies Used

\- Python 3.x

\- Django

\- HTML, CSS, Bootstrap

\- JavaScript (AJAX for dynamic actions)

\- SQLite (default Django DB)



\## Project Structure

media/

&nbsp; ├── designs/

&nbsp; └── profile\_pics/

visionflow/

&nbsp; ├── settings.py

&nbsp; ├── urls.py

&nbsp; ├── asgi.py

&nbsp; └── wsgi.py

vision\_app/

&nbsp; ├── migrations/

&nbsp; ├── static/

&nbsp; │   ├── css/

&nbsp; │   ├── img/

&nbsp; │   └── js/

&nbsp; ├── templates/

&nbsp; ├── admin.py

&nbsp; ├── apps.py

&nbsp; ├── models.py

&nbsp; ├── tests.py

&nbsp; └── views.py



\## Team

VisionFlow was developed as a solo project for the Full-stack Web Development course at Axsos Academy.



Developer: Nada



\## License

This project is licensed under the MIT License. See LICENSE file for details.



