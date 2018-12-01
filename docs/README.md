Welcome to Cornershop's Backend Test documentation!
===================================================
## apps.manager

In this application Nora creates the food dishes, the options that a menu has, and the menu of the day. The menu is composed of options. It has two states 'Draft' and 'Confirmed', the draft state allows Nora to edit the menu as many times as necessary. When this menu is confirmed, an alert is sent by mail to the registered employees in the app, and it also notifies through the Slack # lunch channel.
Nora can see the custom orders of the employees and change the status from "Pending" to "Ready".

##app.employees
The apps.employees is where the menu of the day with its options is displayed, the employee can choose his favorite option and make personalizations, such as changing the size of the dishes and adding to each of them some specification. When you choose an option and an order is generated, by visualizing an ID, with that ID and the employee's RUT you can see the order and review it.