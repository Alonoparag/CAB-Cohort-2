 7. Maria needs to get on a train that leaves from the station D kilometres away in T minutes.
 She can get a taxi that drives at S1 km/h for the price of R €/km or she can walk at S2 km/h for free.

A correct solution will be a function that returns the minimum price she need
to pay the taxi driver or the string “Won’t make it!“.
All the inputs will be positive integers, the output has to be a string containing a number with
 two decimal places – or “Won’t make it!” if that is the case.

It won’t take her any time to get on the taxi or the train.
In non-trivial cases, the need is to combine walking and riding the taxi so that she makes it,
but pays as little as possible.

The input parameters will be in that order:
Distance, Time, Taxi speed, Price rate of taxi per km, Walking speed

def calculate_optimal_fare(dist,time,taxi_speed, taxi_price,walk_speed):
    v_t = taxi_speed
    t_r = taxi_price
    v_w = walk_speed
    time = time/60
    # IF SHE CAN'T MAKE IT WHILE USING THE TAXI THE ENTIRE WAY:
    if time*v_t < dist:
    #     RETURN THE STRING "WON'T MAKE IT"
        return "Won\'t make it!"
    # ELSE:
    else:
    #     FIND THE MAXIMUM TIME MARIA CAN WALK
    #     USE THE FORMULA:
    #         T(MAX)=(DISTANCE-V_1*TIME)/(V_2-V_1)
        t_w = (dist-v_t*time)/(v_w-v_t)
    #     FIND THE DRIVING TIME
        t_taxi = time-t_w
    #     CALCULATE THE DRIVING PRICE
    # RETURN THE TOTAL PRICE
        return t_taxi*v_t*t_r

Example
print(calculate_optimal_fare(10, 50, 30, 10, 6))# Output: 62.50

print(calculate_optimal_fare(100, 50, 30, 10, 6))# Output: “Won’t make it!