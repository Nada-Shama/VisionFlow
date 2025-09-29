🎨 VisionFlow
✨ Welcome to VisionFlow!

Imagine a place where your creative sparks can shine, where your digital masterpieces meet an audience eager to be inspired. That’s VisionFlow! It’s a web-based playground for graphic designers, interior enthusiasts, and digital artists to upload their work, get feedback, and explore others’ creativity. Whether you’re looking to show off your latest design or find fresh inspiration, VisionFlow is your canvas.

🚀 Features

Upload & Share: Post your creations across multiple categories – Graphic Design, Interior Design, Digital Drawing.

Community Love: Like and comment on designs to connect with fellow creatives.

Explore with Ease: Browse designs by category or check out trending works.

Personal Touch: Manage your profile and upload a profile picture.

Sleek & Responsive UI: Works beautifully on desktop and mobile alike.

Real-Time Interaction: Comments and likes update instantly, keeping the community vibrant.

🛠️ Installation

Bring VisionFlow to your local machine and dive into the creative world:

# Clone the repo
git clone https://github.com/nada-shamaa/visionflow.git

# Navigate to the project folder
cd visionflow

# Apply database migrations
python manage.py migrate

# Launch the server
python manage.py runserver


Open your browser at http://127.0.0.1:8000/
 and let the creativity flow!

or open the direct link : https://nadashama.pythonanywhere.com/login/

🎨 Usage

Once you’re in, here’s what you can do:

Register & Create: Sign up and start uploading your designs.

Interact: Like, comment, and inspire others in real-time.

Discover: Explore designs by category and find new creative ideas.

Personalize: Update your profile and showcase your avatar.

Enjoy: Experience a modern, responsive, and friendly interface.

🧰 Tech Stack

Backend: Python 3.x & Django

Frontend: HTML, CSS, Bootstrap

Interactive Actions: JavaScript & AJAX

Database: SQLite (default Django DB)

📂 Project Structure
media/
├── designs/
└── profile_pics/

visionflow/
├── settings.py
├── urls.py
├── asgi.py
└── wsgi.py

vision_app/
├── migrations/
├── static/
│   ├── css/
│   ├── img/
│   └── js/
├── templates/
├── admin.py
├── apps.py
├── models.py
├── tests.py
└── views.py

💡 About the Project

VisionFlow was born from the desire to connect creatives and showcase talent in one interactive space. This solo project was developed for the Full-stack Web Development course at Axsos Academy, with the goal of creating a fun, user-friendly, and community-driven platform.
