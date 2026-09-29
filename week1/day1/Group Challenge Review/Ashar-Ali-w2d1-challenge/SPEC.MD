
##  Spec for creating Recipie box, locally run endpoints  and acceptence tests 

WHY  - Need to create recipie  box ,with 5 endpoints (locally run,synthetic data )

WHAT - Implement the acceptence tests for recepie box. Write the endpoints:

get_recipie  - GET

post_new_recipe -POST 

get_all_recipes -GET

change_recipe  - PUT

remove_recipe  - DELETE



RULES/CONSTRAINTS : 

1.  recipies in recipe list ,which must   have dish name,description,ingredients list and rating 

2. Example in recipe list in synethic data would have
dish_name= "Chocolate Cake" , description="Chocolate sponge cake with cherry ont top and flakes ", ingredients_list="Egg,flour, suger,chocolate baking mix, cherry", rating="4 out of 5"  

3. get_recipie  Must check if dish name is in recepie list, returns a message that it wasnt found

4. create_recipe - Ensure the recipe has dish name, description ,ingredients list and rating 

5. get_all_recipes - returns all recipies in recipie list 

6. change_recipe - Search ingreidents list for Recepie Item, returns successfull or failed. Then PUT changes to each dish_name,ingredients_list or other. 

7. remove_recipe - remove the receipe  from recipe list and returns the dish name. 

8. Out of scope: Do not source data from real place , do not add other endpoints 



TASKS  - 

0. Create recipe list and have 5 synethic examples
Touches:endpoints.py
Verify:meets contraints example

1. Write acceptence tests for 5 endpoints 
Touches: tests folder
Verify: tests created 


2. Implement each of 5 endpoint 
 Touches: endpoints.py 
 Verify: Each endpoint passes its acceptence test. 

