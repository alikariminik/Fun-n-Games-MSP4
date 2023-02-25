# Fun-N-Games README
Here is a link to the website [Fun-N-Games](https://fun-n-games.herokuapp.com/home)

## What is this ReadME for?
This is the ReadMe for the website Fun-N-Games. Fun-N-Games is an e-commerce toystore website built using Django an application with the use of Python, HTML, CSS, JavaScript. The Products, User Accounts and Models are in a SQL Elephant Database and static files such as images and CSS are stored with AWS. 

## Table of Contents
* [User Experience Design (UX)](#UX)
    * [The Strategy Plane](#The-Strategy-Plane)
        * [Site Goals](#Site-Goals)
        * [User Stories](#User-Stories)
    * [The Scope Plane](#The-Scope-Plane)
    * [The Structure Plane](#The-Structure-Plane)
    * [The Skeleton Plane](#The-Skeleton-Plane)
        * [Wireframes](#Wireframes)
    * [The Surface Plane](#The-Surface-Plane)
        * [Design](#design)
            * [Colour-Scheme](#colour-scheme)
            * [Typography](#typography)
            * [Imagery](#imagery)
    * [Features](#features)
        * [ParliamentAPI](#uk-parliament-api )
        * [Planned / Scrapped Features](#planned--scrapped-features)
    * [DataSchema](#data-schema)
    * [Testing](#testing)
      * [Validator Testing](#validator-testing)
      * [Responsiveness](#responsiveness)
      * [Known Bugs](#known-bugs)
    * [Deployment](#deployment)
    * [Credits](#credits)
        * [Resources](#resources)
        * [Code](#code)
        * [Media](#media)

## UX

### The Strategy Plane
* I decided on making an E-Commerce Toy Store for my Milestone Project when browsing for a suitable dataset that fit the requirements of my project. After having spent a good few hours - longer than I had hoped to do so, I came across [Amazon-Products-Dataset](https://www.kaggle.com/datasets/promptcloud/amazon-product-dataset-2020) which was filled with thousands of different products all with photos and prices as well as details on the products. After scanning through this dataset, I noticed that there was an abundance of Toy Products in here so I decided to cut the other 8000 or so items out of this dataset and settle on a Toy Store.


#### User Stories 
* User Stories and their statuses can be found here [UserStories-GitHub-Projects](https://github.com/users/alikariminik/projects/1/views/1)



### The Scope Plane
Features Planned
* A page which displays all of the products in one page.
* A page which only shows products that have a special offer or a discount applied.
* A check out feature which utilises Stripe payments
* An account creation system which meets standard password and account protections such as minimum characters length.
* Responsive Design allowing the user to correctly operate the site across a range of devices the user could potentially use such as Desktop, Laptop, Tablet and Mobiles.
* Be able to Create, Read, Update and Delete data on the database through the website and have these changes reflect instantly on the website (CRUD Functionality)
* The site should be fully accessible for keyboard users
* The site should be fully accessible for screen reader users

### The Structure Plane 
User Story: 
> As a User, I want to be able to search for, filter & sort products in the store

Acceptance Criteria:
* User should be able to search for products using the search bar, filter by catergories and sort by price.

Implementation:
* A Search Bar, NavBar with links to filter by categories will available on all pages of the site. Sort options will be confined to products pages.

User Story: 
> As a User, I want to be able to view all products which are on sale so that I can make savings by purchasing only discounted products.

Acceptance Criteria:
* User should be able to view only products which have a sale or special offer attached to them.

Implementation:
* A seperate products page is created which will only show products on sale and ones which have a special offer on them.

User Story: 
> As a User, I want to be able to log in to my account so that I can review my past orders and save default delivery details

Acceptance Criteria:
* Users should be able to view previous orders and saved default delivery details. 

Implementation:
* A profile page to be implemented for registered users which will display past orders and currently saved delivery information with the option to update this through a form.

User Story:
> As a User, I want to receive email confirmations when I create an account so that I know the account creation was successful.

Acceptance Criteria:
* When a user creates an account, an email verifying this is sent out. 

Implementation:
* To be implemented through Allauth and Django.

User Story:
> As a Store Owner, I want to be able to add new products to my store so that I can offer the news toys to customers

Acceptance Criteria:
* Superuser can add new products to the store database and these will immediately show on the website.

Implementation:
* An Add Product Form, accessible only to Superusers that will allow for new products to be created when a name, price, and details details are given.

User Story: 
> As a Store Owner, I want to be able to edit the details of existing products in the store so that I can make changes where necessary (such as price increases / decreases or product name)

Acceptance Criteria:
* Superuser can edit any of the fields of exisiting products

Implementation:
* An Edit Product Form, accessible only to Superusers that will allow for name, price, details, image etc changes.

User Story:
> As a Store Owner, I want to be able to put products of my choice onto sale and dynamically set the sale price so that I can have frequently reduce product prices in order to increase the likelihood of sales

Acceptance Criteria:
* Superusers should be able to put any product on sale or attach a special offer to them. 

Implementation:
* Through the same Edit Form mentioned in the previous user story or through the django-admin, sales and deals can be attached to any product of the Store Owner's choice.

User Story:
> As a Store Owner, I want to be able to allow users to create accounts using their social media accounts so that I can make it quicker for users and increase the likelihood that they will use our store.

Acceptance Criteria:
* Users can create an account through their existing social media accounts

Implementation:
* To be implemented through Allauth.

### The Skeleton Plane
#### Wireframes
I utilised Balsamiq to produce my wireframes of how the app homescreen would appear across different devices. This was not stuck to.l

Mobile Device Wireframes 
 ![Mobile Device Home](media/wireframes/wireframe-desktop-home.png)
Tablet Device Wireframes
 ![Tablet Device Home](media/wireframes/wireframe-desktop-home.png)
Desktop Device Wireframes
 ![Desktop Device Home](media/wireframes/wireframe-desktop-home.png)


### The Surface Plane
#### Design 
The area I felt this project lacked in the most was the design. I have relied very heavily on Bootstrap which has been extremely helpful for quick development whilst ensuring responsiveness and performance across varying screen views. However, I feel as though had I had more time to spend on this project, I would have improved the design more by adding more of my own custom CSS and utilised an eye-catching colour pallet 

![StoreLogo](https://www.freelogodesign.org/)

#### Imagery
The images for the products are obtained directly from where they are hosted online on Amazon. This was a downside of the dataset I found in that it did not have a file with images seperate. This can can effect performance when loading All Products as there are over 2000 images being downloaded. Additionally, if the product image was ever removed from its original hosting site (for which I have no control over) then this site would not be able to retrieve the product image. However, as a safeguard for this, there is a backup image. 

### Planned / Scrapped Features
When starting out, I had planned to allow for users to register accounts through their Social Media accounts. This is outlined in one of the User Stories. I believe that this feature would have been a nice touch and if it were utilised in a real store, then it is likely to increase the chance of custom as an account can usually be created in just a couple of taps / clicks. 

### Languages Used

-   [HTML5](https://en.wikipedia.org/wiki/HTML5)
-   [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
-   [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
-   [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

### Frameworks, Libraries & Programs Used
-   [Django](https://www.djangoproject.com/) 
    - Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.
-   [Font Awesome:](https://fontawesome.com/)
    - Font Awesome icons were used across the pages which acted as buttons to aid navigation for the user. The Font Awesome Icons themselves were also added for aesthetic and UX purposes.
-   [Bootstrap 5.3](https://getbootstrap.com/)
    - Bootstrap was used to assist with the responsiveness, layout, design and JavaScript components on the website
-   [elephantsql](https://www.elephantsql.com/)
    - The Relational Database was hosted on elephantsql and its data is obtained through the use of
-   [AWS](https://aws.amazon.com/)
    - Used to store images and static files.

## Data Schema
### Products


### Profiles
#### UserProfile
-   User = A one-to-one relationship with User from Django Allauth "User"
-   default_street_address1 = Character Field storing first line address
-   default_street_address2 = Character Field storing second line address
-   default_town_or_city = Character Field storing town / city name
-   default_postcode = Character Field storing postcode / Zip
-   default_county = Character Field storing county / state
-   default_country = Dropdown selector used to capture country
-   default_phone_number = Character Field storing mobile phone number

### Products
#### Product 
-   uniq_id =IntegerField(null=True, blank=True)
-   name =254)
-   category = A many-to-many relationship with the Category model
-   sub_category1 = Character Field. Initial plans to incorporate sub-categories of products but this was mot implemented.
-   sub_category2 = Character Field. Initial plans to incorporate sub-categories of products but this was mot implemented.
-   price = Decimal field which stores product price.
-   product_description = Character field which stores product description. 
-   product_url = URL Field which stores product image.
-   coupon_codes = A many-to-many relationship with the CouponCode model. Allows for Discounts to be applied to products.
-   deal = A many-to-many relationship with the Deal model. Allows for Special Offers to be applied to products.

#### Category
-   name = Character field containing category name. Allows for filtering by category in the store.
-   friendly_name =  Character field containing category name displayed in an user-friendly name.

#### CouponCode
-   Percentage = Integer field which will deduct a given percentage from the product price. User to apply sales. 
-   Name = Character field use to render the value of the saving in percentage.
-   discount_amount = Not used Character field. Initial idea was to calculate value of the saving between old and sale price for a product.

#### Deal
-   name = Character field capturing name of Deal (3for2).
-   eligible_quantity = IntegerField used to calculate if Special Offer criteria is met (3). 
-   saved_quantity = IntegerField used to calculate if Special Offer criteria is met (For every 3 in Cart, deduct 1).

## Testing 
### Behaviour Driven Development (BDD)

### Validator Testing
* HTML
  *     [W3C Validator](https://validator.w3.org/nu/)

* CSS
  *     [Jigsaw Validator](https://jigsaw.w3.org/css-validator/validator)

* JSlint
  *     [JSlint Validator](https://www.jslint.com/)

### Responsiveness
Vigorous testing was conducted throughout the development process to ensure that the site maintained responsiveness as more elements were added on. Using developer tools and adjusting screen dimensions, I have checked to ensure that all content displays clearly over a variety of screen sizes - primarily on the Mobile, Tablet and Monitors. As mentioned above, media queries were added to correct responsiveness failings from Materialize.

### Known Bugs
- No known bugs at this time.


## Credits

#### Resources 
- Code Institute course material
- Code Institute Mentor
- [CodeInstitute-ReadME](https://github.com/Code-Institute-Solutions/SampleREADME)


#### Media 
- [HeroImage]
- [FnGLogp](https://www.freelogodesign.org/) Generated from freelogodesign.org
- [No-Image-Placeholder](https://commons.wikimedia.org/wiki/File:No-Image-Placeholder.svg)