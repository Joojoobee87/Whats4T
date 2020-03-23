# Whats4T?
Whats4T? is a website which hosts a collection of recipes created and maintained by its registered users. Inspiration for this site came from my own experiences as a mother who enjoys cooking tasty yet healthy dishes for my family at mealtimes. I regularly battle with the question of what to make for tea, particularly when time is of the essence due to work, school runs and extra-curricular activities and consequently tend to stick to my tried and tested repertoire of recipes. I wanted to develop a site that would give users quick access to a host of ‘teatime’ recipes, where users could browse key words based on ingredients in their store cupboard, enabling them to expand their repertoire and provide something new and different for them to try out.
The original and adapted brief for this milestone project can be found [here](documentation/MS3_Project_Idea_1.docx "Original Project Brief 1")

## UX Design
The website is aimed at a diverse demographic of users, essentially anyone who wants inspiration for daily meal times and who wants to find some new dishes to try out. Users can range from people visiting the site ad hoc to search and view recipes, to people who want to be more actively involved by contributing to the collection already available. 
### User stories
As a user, I want to:

	Browse a full list of recipes to gain inspiration for new dishes
	View popular recipes including ingredients and method
	Create and add new recipes to the collection
	Search the full collection of recipes using keywords or specific ingredients
	Search the full collection for recipes with a maximum combined prep and cooking time (total time)
	Update recipes I have added to the collection
	Remove recipes I no longer want to make available to other users
	View a full list of recipes I have added to the collection
	View reviews and comments made by other users who have tried and tested recipe*
	Save recipes to my profile to access at a later date*

As a website owner, I want to:

	Offer advertising space on website to attract advertisers and increase revenue stream

As an advertiser, I want to:

	Place adverts on website to attract users to my website, product etc

**These user stories were ruled out of the initial project scope due to time constraints however are features that could be implemented with further development time*
### Wireframes 
Wireframes for the project were drafted on the Balsamiq Wireframes application.

The wireframes and notes to accompany them can be accessed here:
A [link](documentation/Whats4T.pdf "Whats4T Balsamiq Wireframes")

## Features
### Existing Features
### General features
	**Navigation bar** – the navbar assists the user with ease of navigation around the site. Where users are not logged in, there will be a ‘login’ and ‘register’ nav link to the respective pages. Where users are logged in, they will be presented with an additional My Recipes nav link which will drop down to reveal additional navigation items to view recipes in their collection and create new recipes. There will also be the option to logout which will terminate their session
	**Footer** – the footer hosts font awesome icons for the user to navigate out to the respective social media platform. 

### Whats4T Homepage (index.html)

	**Welcome and summary** - The initial landing page is the entry point for users to the site and provides them with a welcome message as an introduction to the site and a brief summary of what they are likely to find here.

	**Background image** – gives the site visual impact, attracting their attention initially with colours and colourful raw ingredients.

	**Recently Added section** – displays to the user the 4 most recently added recipes to the database, for regular usersto the site, this will give them an indication as to whether any new recipes have been added since their last visit.
	**Most Viewed section** – displays to the user the 4 most viewed recipes in the database, so the user can quickly establish what could be some of the more popular recipes to view

### Browse (recipes.html)

	**Browse all recipes** – the Browse page allows the user to browse through the entire collection of recipes available in the database. The results are displayed 10 per page and pagination buttons are present at the bottom of the page to allow the user to navigate between pages of results
	**Search functionality** – there are two search fields which are displayed at the top of the page
**Keywords** – this search field allows a user to search for keywords such as recipe ingredients or perhaps tags such as vegetarian. Results are displayed to the user in order of how closely they match the search criteria entered
**Total Time** – this search field allows a user to search for recipes with a maximum total time in minutes. Results are displayed to the user up to and including the total time entered and are ordered ascending from shortest to longest time

### Recipe (showrecipe.html)

	**View selected recipe** – the user is redirected to this page when they click on the ‘view’ button inset within any of the recipe results displayed. This could be via the homepage, browse page or view my recipes. The user is presented with full details of the recipe including image, title, summary, ingredients, method, tags, views and time values

### Create a recipe (createrecipe.html)

	**Create recipe form** – the user is presented with a blank template in which to enter their recipe details. The form is clearly labelled and provides the user with some placeholder text on the type content required for each.
	**Add Recipe** – the add recipe button will allow the user to submit their new recipe to the database which then returns to user to the View My Recipes page and displays the new recipe

### My Recipes (myrecipes.html)

	**My Recipes** – the user is presented with all of the recipes they have added to the database, presented with the image, title and summary detail
	**View** – the user can click the view button to view full details of their recipe (see above showrecipe.html)
	**Edit** – the user can click the edit button which redirects them to the Update Recipe page where they can edit any of the fields held against the selected recipe in the database (see editrecipe.html below). 

### Edit recipe (editrecipe.html) 

	**Edit recipe form** – details of the selected recipe are displayed to the user in the same format as the create recipe form. 
	**Update button** – allows the user to submit the amended recipe details to the database, they are then returned to the My Recipes page
	**Back** – allows the user to return to the My Recipes page without making any amendments to the recipe
	**Delete** – allows the user to delete the selected recipe. On click, the user is redirected to a modal box which asks for confirmation that they wish to delete. 
	**Confirmation modal** - Selecting Yes deletes the recipe and returns the user to the My Recipes page. Selecting ‘No’ returns the user to the Edit Recipe page.

### Register (register.html)

	**Registration form** – allows the user to be able to register their details and gain access to additional functionality on the site including creating and sharing their own recipes with other users

### Login (login.html)

	**Login form** - allows the user to be able to login using their registered details to access additional functionality including creating and sharing their own recipes with users as well as updating and deleting recipes they have already contributed.
### Features left to implement
	Recipe (reviews) – ability for users to add reviews to the recipes they have tried out, which in turn would then be available to other users viewing the recipe
	Saved recipes – ability for users to save recipes they have viewed to a list from the collection which they can access at a later date when logged in

## UX Design
I am a designer by nature and have a keen interest in how things look and appear so I strive to design and develop sites that I would enjoy viewing and interacting with myself. I use technology a lot in my daily life including websites and applications both personal and work based so I understand the importance of UX Design and the impacts of not getting it right.

Throughout the course I have done a lot of extended reading on UX and design principles including reading blogs from various professionals and experts in the field and have developed this project trying to adhere to some of the key practices.

### Structure and Flow

In order to ensure a clear, ordered structure to the information displayed on the web pages and to guarantee a more responsive design, I utilised **Bootstrap** frameworks grid system which I decided would be the best method to display a varying number of results from the database. As the content can vary from page to page, and depending on the search queries performed by users of the site, the results needed to be displayed in a simple and visually appealing format to encourage user browsing. 

With vertical flow and scrolling, the results occupy 1 or 2 columns per row depending on the width of device and a maximum number of 10 results are displayed per page to allow the user to browse and navigate around more effectively. There is clear separation of content with horizontal lines and headings to give distinction between sections and results.

### Navigation

**Bootstrap** has been further utilised for its responsive navigation bar, showing the main page links and a dropdown field presenting 2 further navigation links which are displayed to users upon login. The navigation bar is compressed to a hamburger style menu for smaller mobile devices. Pages are clearly labelled so the user can anticipate what to expect when navigating around. Links to pages are also included in page content where appropriate, for example the Login page has a link to the Register page for users who are not yet registered, and likewise, the Register page links to the Login page for users who already have an account.

Action buttons are used throughout the site to perform a series of CRUD (Create, Read, Update and Delete) actions. On the Update Recipe page, the user is presented with options to ‘Update’, ‘Delete’ or go ‘Back’ to the My Recipes page, rather than having to click back through the links on the main navigation bar. When a recipe is created or updated, the site automatically returns the user to the My Recipes page where the new or updated information is displayed.

### Forms

**Bootstrap** forms have been used for the various forms included throughout the site. The forms are structured in a vertical style with field sizes appropriate to the content they should contain. For example, the ingredients and method fields are larger than others as these are likely to hold multiple lines of content. The 3 ‘time’ fields have been structured in a row of 3 equal columns as they require much less space, containing only numerical values. 

Field labels have been placed consistently above the related field and placeholder text has been included with the field to guide the user on the type of content required.

The ‘type’ attribute of the input field ensures that the user is only able to enter the relevant type of content, for example, the time boxes are number types and will only allow numerical values, or the user can click on the arrows to increase / decrease numerical values.

**WTForms** library has been used to provide form validation, ensuring users can only enter the correct type of data. The form fields provide user feedback and detail on errors against the relevant field, to ensure that the user clearly understands the error made and can correct before resubmission. 

### Typography

I had an idea of the font style I’d like to include in this project, something clear and simple with a soft undertone. I browsed **Google Fonts** and selected several for my shortlist, then decided upon Catamaran as the font choice for this project.

Font sample:
![](/static/images/Catamaran.jpg)

### Colour

**Coolors** (https://coolors.co/) was used to generate and experiment with different colour choices and colour combinations. I wanted to use a vibrant but fresh colour and apply it as consistent branding across the site. I wanted a colour that would be unlikely to appear in images of recipe dishes to ensure enough contrast between branding and recipe images. The final colour selections can be seen below, with #56A3A6 chosen for the project.

Colour pallet:
![](/static/images/Whats4T_colours.jpg)

A single colour scheme has been maintained throughout for consistency, applied to header and footer, text headings and buttons with further splashes of colour introduced as a result of image content. I considered the use of more than one colour for the project but thought it could risk the site looking too busy and distracting from the content and purpose. The inclusion of vibrant recipe images throughout the site introduces enough colour without it needing anything further.

A fixed background image was selected to create visual appeal, showing a variety of different and colourful ingredients, hoping to inject inspiration and capture the user’s attention. The background image has been overlaid with a white section to hold the main content of the page, providing contrast from the background image and to make text content and additional images clearly visible.

### Icons

**Font Awesome** has been utilised for the various icons in use throughout the site. These include the social media icons for Facebook, Twitter and Instagram as well as icons for use in the recipes to display prep, cooking and total time and numbers of views of the recipe. The icon images are relevant to their function, for example a ‘clock’ icon depicts time and an ‘eye’ icon for views.

The social media icons have been included in the footer in a linear format with clear distinction between them and direct users to the relevant social media site upon click.


## Technology
In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.
	HTML
	CSS
	Python
	Flask framework
	Flask Login
	WTForms library
	Jinja template
	MongoDB
	Bootstrap
	Font Awesome
	Coolors (https://coolors.co/)
	Google Fonts

## Testing
I created a testing framework in excel with specific testing scripts and scenarios to test out on each of the pages / functions included throughout the project. The framework included the page / function being tested, the test carried out and the expected result.
The project was designed to be responsive, adapting structure and formatting according to the user’s device. Consequently, testing needed to be carried out on a variety of different sized devices as well as on different browsers to ensure that the pages and functionality responded as expected across a range of different technologies.
Where tests failed, the relevant alterations were made to the code, changes saved and committed and the test was repeated to ensure it responded correctly.
A link to the Milestone 3 Testing excel can be found [here](documentation/MS3_Testing.xlsx "Milestone 3 Testing – Whats4T?")


## Deployment
**GitPod and GitHub**
The project was written in GitPod, a new Whats4T repository was created in GitHub and regular commits were made throughout the project build and pushed out to the repository.

**Mongo DB**
Mongo DB Atlas was used to create the Whats4T database for the project. Within the Whats4T database, 2 collections were created including Recipes to hold the data relating to the recipes and Users to hold data about users, namely their login details.
The database and collection structure can be found [here](documentation/Whats4T_Database_Structure.xlsx "Whats4T? Database Structure")

**Flask Login**
Login functionality has been implemented to allow for encryption of passwords, the secrets module was imported on the command line and the secrets.token_hex(16) to obtain a unique 16 character random key to use. A new 16 character key was regenerated and updated towards the end of the project as the value was committed to the GitHub repo via the app.py file prior to it being moved to the env.py file

**Environment Variables**
The MONGO_URI and SECRET_KEY environment variables have been added to the env.py which in turns has been added to the .gitignore file to ensure no visibility of this data

**Heroku**
Heroku has been used to deploy the application. Steps taken to deploy the code can be found [here](documentation/Heroku_Deployment.docx "Heroku Deployment")
## Credits
### Content
**Bootstrap** has been utilised extensively throughout the site including navigation, forms, modals and responsive design

**BBC Good Food** has been used for the majority of recipes already added to the collection including content (title, ingredients and method) and images

**Corey Schafer** YouTube videos were instrumental is enhancing my understanding of the Flask framework
### Media
All recipe images initially added to the collection have been taken from **BBC Good Food** site, see https://www.bbcgoodfood.com/

Homepage image is courtesy of **Marco Verch**, source:
https://foto.wuestenigel.com/notebook-with-a-large-selection-of-ingredients-for-cooking/?utm_source=47287625671&utm_campaign=FlickrDescription&utm_medium=link

**Lakeland** – image used for Lakeland advert on showrecipe.html
https://www.lakeland.co.uk/around-the-home/cleaning-products/

### Acknowledgements
I followed the brief of Project Example 1 given by Code Institute and drew from my own experiences of family mealtimes to develop my ideas for the site.

I am grateful to my mentor Spencer Barriball who was instrumental in helping me get set-up and running on my Milestone 3 project and reigniting my motivation for the course.




