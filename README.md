# Flask Web Application Project

**Course**: INFO-I 211, Information Infrastructure II, Spring 2023 <br>
**Institution**: Indiana University <br>
**Final Product**: [Outdoor Adventures](https://cgi.luddy.indiana.edu/~lsgulsen/I211_project.cgi/)
> Imported from my IU enterprise account github.iu.edu/lsgulsen

## Project Overview

Create a simple application for an outdoor company where all of their outdoor adventure trips and members are displayed online. The management team wants a website where they can create, edit, and delete trips and members.

### Learning Objectives
- Install a complete Flask environment on your local machine.
- Effectively use Git tools to manage your source code
- Utilize routes and templates to create web pages in Flask
- Access and parse outside data to add dynamic content to web pages in Flask

## Technologies and Tools Used

- Python
- Flask
- Jinja
- HTML/CSS
- MySQL

## Features and Functionality

### Dynamic Trip Management
- **Create**: Allows the management team to add new outdoor adventure trips, including details like trip name, location, duration, and cost.
- **Edit**: Facilitates updating existing trip information to reflect changes in itinerary, pricing, or other details.
- **Delete**: Provides the option to remove trips that are no longer offered, ensuring the website reflects current offerings.
### Member Directory
- **Member Registration**: Allows management to add new members and add their personal informations such as name, email, address, phone number, and date of birth.
- **View Members**: Allows both management and members to view a directory of all members, enhancing the community feel.
### Interactive Trip Catalog
- **Trip Display**: Lists all available trips, with detailed pages for each trip that include descriptions, itinerary, cost, and requirements.
- **Member Association**: Within the detailed page for each trip, members who are attending the trip are listed, and are able to be deleted. Members not on the list are able to be added as well.
### Responsive Design
- **Bootstrap**: The website is designed to be responsive, ensuring a seamless experience across devices, from desktops to mobile phones.
### Backend Management
- **MySQL Database**: Utilizes a MySQL database to store and manage all data related to trips and members securely.
- **Flask and Jinja Templates**: Implements Flask routes and Jinja templates to serve dynamic web pages based on the database content.

## Challenges and Learnings

One of the main challenges was changing the site to use a MySQL database instead of a CSV file. Adding, editing, and deleting data, and having the changes made in the database and not only in the browser, was a challenge as well.

## Final Outcome

The project met all of the course requirements and is a fully funcitonal Flask application. It was a valuable learning experience in database management.

## Acknowledgments
Professor Matt Hottel and Professor Erika Lee, for guidance and insights
