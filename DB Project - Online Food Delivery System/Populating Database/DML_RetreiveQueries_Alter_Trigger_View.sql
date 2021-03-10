/* DML Commands*/
/* Insert new tuple with values (1,"Vanilla Milkshake") into Food Table */
insert into food values(1,"Vanilla Milkshake");

/* Update Phone number of Diana T Prince 3183333333 with 3183333334*/
update cust_phone cp join customer c on cp.email_id = c.email_id set Phone=3183333334   
 where Fname='Diana' and Mname='T' and Lname='Prince' and Phone='3183333333';

/*  Delete Vanilla Milkshake food item from Pizza Hut */
delete food from food join restaurant on food.Res_ID=restaurant.Res_ID where Name="Pizza Hut" and Item_name="Vanilla Milkshake";

/* Retreival Queries */
/*Retreive names of delivery person whose salary is between 500 and 550*/
select Name from delivery_man where Salary between 500 and 550;

/* Show Order_Summary of failed payments*/
select Order_Summary from orders where Order_ID = 
any(select order_id from order_payment join payment on order_payment.p_id=payment.p_id where payment_status="Failed");

/* Retrieve Total Amount made by each restaurant from payments */
select Res_ID, SUM(Paid_Amount) as TOTAL from payment where Payment_Status="Received" group by Res_ID ;

/*Show names of restaurant who got minimum orders */
select restaurant.name from restaurant join orders on orders.res_id=restaurant.res_id group by orders.res_id having count(orders.res_id)<=all
(select count(res_id) from orders group by res_id);

/*Display Customer Fname, Lname who didn't order Chicken */
select distinct Fname,Lname from orders join customer on email_id=user_email_id where Order_Summary NOT LIKE '%Chicken%';

/* Change datatype of Reward_Points and  Standard_Delivery_Charges using alter command*/
alter table customer modify Reward_points DECIMAL(10,2);

alter table customer modify  Standard_Delivery_Charges DECIMAL(10,2);

/* Create a Trigger to update the Reward_Points or Standard_Delivery_Charges of Customer based on the Order made and Customer_Type */
DELIMITER $$
CREATE TRIGGER RewardPoints
AFTER INSERT ON Orders
FOR EACH ROW 
BEGIN
    DECLARE N VARCHAR(50);
    DECLARE S DECIMAL(10,2);
    SET N = (SELECT Cust_Type from CUSTOMER where Email_ID=NEW.User_Email_ID);
    SET S = (SELECT Standard_Delivery_Charges from CUSTOMER where Email_ID=NEW.User_Email_ID);
    SET S = S-(NEW.Order_Amount/100);
	IF N='Premium' then
		update customer set Reward_Points=Reward_Points+(NEW.Order_Amount/10) where Email_ID=NEW.User_Email_ID;	
    ELSE IF(S<0) then 
		update customer set Standard_Delivery_Charges=0 where Email_ID=NEW.User_Email_ID;
	ELSE
		update customer set Standard_Delivery_Charges=S where Email_ID=NEW.User_Email_ID;	
    END IF;
    END IF;
END$$
DELIMITER ;

/* Create a view that gives information about Customer Name, Order Summary and Delivery guy name */
CREATE VIEW DELIVERY_SUMMARY
AS SELECT CONCAT(Fname,' ',Mname,' ',Lname) as CUSTOMER_NAME, ORDER_SUMMARY,Name as DELIVERY_MAN
   FROM CUSTOMER C, ORDERS O, DELIVERY_MAN D,ORDER_DELIVERY OD
   WHERE OD.User_Email_ID=C.Email_ID AND OD.Order_ID = O.Order_ID and OD.DM_ID=D.Emp_ID;

/* Create a view that gives Customer name and list of phone numbers they having(in one column i.e.., concat phone numbers) */
CREATE VIEW CUST_PHONE_NUMBERS
    AS select concat(Fname,' ',Mname,' ',Lname) as CUSTOMER_NAME, GROUP_CONCAT(Phone) as LIST_OF_PHONE_NUMBERS 
    from CUSTOMER C, CUST_PHONE CP where C.Email_ID=CP.Email_ID group by C.Email_ID;

/* Create a view that gives information of Delivery guys who didn't get assigned any orders to delivery from their restaurants */
CREATE VIEW REST_DM
    AS select D.Name as DELIVERY_GUY, R.Name as RESTAURANT from DELIVERY_MAN D, RESTAURANT R 
    where D.Res_ID = R.Res_ID and Emp_ID not in (select DM_ID from ORDER_DELIVERY);
