# home_watering_system

External Constraints:
    Because of water pressure, only one area can run at a time
    
Interal Constraints: (To keep things simple, or to speed development)
    the system will only work with granularity of 15 minute blocks of time
    the system will only update every 15 seconds
    the system will run off of a weekly schedule of time slots
    
    
System design:
    python flask api
        [start up/restart]
            deactivate()
            resets flow meter
            
        activate(area)
            if area aleady activated, return
            
            deactivate()
            resets flow meter
            activates the area requested for the next 15 minutes
            
        deactivate()
            deactivates all areas temporarily for the current interval
            ex. someone is at the door, something broke and needs a quick fixing
            
        update()
            load time_period from storage

            if area exists
                activate(area)
            else
                deactivate()
            
        set(day, time_period, area)
            if area is null
                clear day/time_period in storage
            else
                set day/time_period in storage
            
            update()
            
            
    
    cron job every 15 sec
        curl flask api -> update()


