import pygame
import os
import random

class Players:
    instances_list = []
    def __init__(self, player_num, control_board_object, planet_image, ship_image):
        self.instances_list.append(self)
        
        self.player_num = player_num
        self.control_board_object = control_board_object
        self.ships_list = []
        self.planets_list = []
        self.planet_image = planet_image
        self.ship_image = ship_image
        
        self.ship_damage = 35
        self.ship_start_health = 20
        self.ship_max_health = 100
        self.ship_health_regen_rate = 5
        self.ship_scan_range = 0
        self.ship_fire_range = 0
        self.ship_speed = 1
        
        self.planet_damage = 20
        self.planet_max_health = 100
        
        self.plasma_defence = 0
        
        self.tech_object = None
        
        self.sci_resource = 3
        self.sci_resource_modifier = 0
        self.prd_resource = 3
        self.prd_resource_modifier = 0
        
        self.enemies_num_list = []
        for i in [1,2,3,4]:
            if i != self.player_num:
                self.enemies_num_list.append(i)
        
        self.alliances_list = []
        
    def harvest_resources(self):
        for planet in self.planets_list:
            self.sci_resource +=  planet.sci_resource + self.sci_resource_modifier
            self.prd_resource +=  planet.prd_resource + self.prd_resource_modifier
            
    def grab_random_tech(self):
        random_tech_selection = self.tech_object.grab_random_tech()
        
        
        
class Ships:
    instances_list = []
    instances_id_list = []
    ship_counter = 0
    
    sci_cost = 1
    prd_cost = 5
    
    def __init__(self, image, ship_id, hex_vertice, hex_object, HexTiles, conversions, player_object):
        self.instances_list.append(self)
        self.instances_id_list.append(ship_id)
        Ships.ship_counter += 1
        
        self.ship_num = Ships.ship_counter
        
        self.image = image
        #self.xxyyzz = xxyyzz
        #self.xy = xy
        self.ship_id = ship_id
        self.hex_object = hex_object
        self.hex_vertice = hex_vertice
        self.player_object = player_object
        self.xy = self.hex_object.shipDrawVerts[self.hex_vertice]
        
        
        self.width = int(HexTiles.edge_radius * 3/4)
        self.height = int(HexTiles.edge_radius* 3/4)
        self.sprite = pygame.transform.scale(pygame.image.load(os.path.join("images", "ships", self.image)),(self.width,self.height))
        
        self.damage = self.player_object.ship_damage
        self.health = self.player_object.ship_start_health
        self.max_health = self.player_object.ship_max_health
        self.health_regen_rate = self.player_object.ship_health_regen_rate
        self.scan_range = self.player_object.ship_scan_range
        self.fire_range = self.player_object.ship_fire_range
        self.speed = self.player_object.ship_speed
        
        self.plasma_defence = self.player_object.plasma_defence
        
        #for hex in HexTiles.instances_list:
        #    if self.xxyyzz == hex.xxyyzz:
        #        self.hex_object = hex
        
    def draw_ship(self, screen):
        if self.health <0:
            self.health = 0
        if self.health > self.max_health:
            self.health = self.max_health
        self.xy = self.hex_object.shipDrawVerts[self.hex_vertice]
        #pygame.transform.scale(pygame.image.load(os.path.join("images", "planets", self.image)),(self.width,self.height))
        screen.blit(self.sprite, (int(self.xy[0] - self.width/2), int(self.xy[1] - self.height/2)))
        self.health_pct = 254*min(self.health/self.max_health,1)
        pygame.draw.circle(screen,
                           (int(254-self.health_pct),int(self.health_pct),0),
                           [int(self.xy[0]), int(self.xy[1])], int(self.width/2)+3, 1)
    
    def scan_area(self):
        if self.scan_range == 0:
            self.hex_object.visible = 1
        else:
            for hex in self.hex_object.neighbours_object_list:
                hex.visible = 1
    
    def regenerate_health(self):
        self.health = min(self.health+self.health_regen_rate, self.max_health)
        
    def delete_destroyed(self):
        #destroy the ship once it reaches <2 health
        if self.health <2:
            for x , ship in enumerate(Ships.instances_list):
                if ship.ship_num == self.ship_num:
                    del Ships.instances_list[x]
                    del Ships.instances_id_list[x]
                    pygame.mixer.music.load(os.path.join("audio", "shipDestroyed.wav"))
                    pygame.mixer.music.play()
        
    def shoot_enemy_ships(self,Ships):
        for enemy_ship in Ships.instances_list:
            # is the ship out of range?
            if enemy_ship.hex_object.xxyyzz != self.hex_object.xxyyzz:
                continue
            #if ship.fire_range == 0:
            #    if enemy_ship.hex_object.xxyyzz != self.hex_object.xxyyzz:
            #        continue
            #else:
            #    if enemy_ship.hex_object.xxyyzz not in self.hex_object.neighbours_xxyyzz_list:
            #        continue
            # is the ship an ally?
            if enemy_ship.player_object.player_num in self.player_object.alliances_list:
                continue
            # is the ship yours?
            if enemy_ship.player_object.player_num == self.player_object.player_num:
                continue
            enemy_ship.health -= int(self.damage * random.uniform(0, 1))
            pygame.mixer.music.load(os.path.join("audio", "laserFire.wav"))
            pygame.mixer.music.play()
        
    def shoot_enemy_planets(self,Planets):
        for enemy_planet in Planets.instances_list:
            # is planet out of range?
            #if enemy_planet.xxyyzz != self.hex_object.xxyyzz:
            #    continue
            if self.fire_range == 0:
                if enemy_planet.xxyyzz != self.hex_object.xxyyzz:
                    continue
            else:
                if enemy_planet.xxyyzz not in self.hex_object.neighbours_xxyyzz_list:
                    continue
            # is planet owned?
            if enemy_planet.player_object is not None:
                # ... by an ally?
                if enemy_planet.player_object.player_num in self.player_object.alliances_list:
                    continue
                # ... by you?
                if enemy_planet.player_object.player_num == self.player_object.player_num:
                    continue
            enemy_planet.health -= int(self.damage * random.uniform(0, 1))
            pygame.mixer.music.load(os.path.join("audio", "laserFire.wav"))
            pygame.mixer.music.play()
        
    def capture_enemy_planets(self,Planets):
        for enemy_planet in Planets.instances_list:
            # is the planet currently too powerful to capture?
            if enemy_planet.health >3:
                continue
            # is planet out of range?
            if enemy_planet.xxyyzz != self.hex_object.xxyyzz:
                continue
            # is planet owned?
            if enemy_planet.player_object is not None:
                # ... by an ally?
                if enemy_planet.player_object.player_num in self.player_object.alliances_list:
                    continue
                # ... by you?
                if enemy_planet.player_object.player_num == self.player_object.player_num:
                    continue
            enemy_planet.process_capture(self.player_object)
            pygame.mixer.music.load(os.path.join("audio", "capturePlanet.mp3"))
            pygame.mixer.music.play()
        
        
        
        
        
class Planets:
    instances_list = []
    def __init__(self, image, xxyyzz, HexTiles, GameBoard, conversions, player_object):
        self.instances_list.append(self)
        
        self.image = image
        self.xxyyzz = xxyyzz
        self.xy = list(conversions.cubic_to_cart(self.xxyyzz, HexTiles, GameBoard))
        self.player_object = player_object
        
        self.width = int(HexTiles.edge_radius)
        self.height = int(HexTiles.edge_radius)
        self.sprite = pygame.transform.scale(pygame.image.load(os.path.join("images", "planets", self.image)),(self.width,self.height))
        
        self.sci_resource = 3
        self.prd_resource = 3
        
        self.health = 2
        self.max_health = 100
        self.damage = 20
        self.health_regen_rate = 5
        
        self.plasma_defence = 0
        
        for hex in HexTiles.instances_list:
            if self.xxyyzz == hex.xxyyzz:
                self.hex_object = hex
        
    def draw_planet(self, screen):
        #pygame.transform.scale(pygame.image.load(os.path.join("images", "planets", self.image)),(self.width,self.height))
        screen.blit(self.sprite, (self.xy[0] - int(self.width)/2, self.xy[1] - int(self.height)/2))
        self.health_pct = 254*max(min(self.health/self.max_health,1),0)
        pygame.draw.circle(screen,
                           (int(254-self.health_pct),int(self.health_pct),0),
                           [int(self.xy[0]), int(self.xy[1])], int(self.width/2)+3, 1)
    
    def regenerate_health(self):
        self.health = min(self.health+self.health_regen_rate, self.max_health)
        
    def process_capture(self,player):
        self.player_object = player
        self.damage = player.planet_damage
        self.max_health = player.planet_max_health
        self.plasma_defence = player.plasma_defence
        self.image = player.planet_image
        self.sprite = pygame.transform.scale(pygame.image.load(os.path.join("images", "planets", self.image)),(self.width,self.height))
        
    def shoot_enemy_ships(self,Ships):
        for enemy_ship in Ships.instances_list:
            # is the ship out of range?
            if enemy_ship.hex_object.xxyyzz != self.hex_object.xxyyzz:
                continue
            # is planet owned?
            if self.player_object is not None:
                # ... by an ally of the enemy ship?
                if enemy_ship.player_object.player_num in self.player_object.alliances_list:
                    continue
                # ... by the owner of the enemy ship?
                if enemy_ship.player_object.player_num != self.player_object.player_num:
                    continue
            enemy_ship.health -= int(self.damage * random.uniform(0, 1))
            pygame.mixer.music.load(os.path.join("audio", "laserFire.wav"))
            pygame.mixer.music.play()
        
        
class Techs:
    instances_list = []
    def __init__(self, player_object, HexTiles):
        self.instances_list.append(self)
        
        self.player_object = player_object
        #self.width = int(HexTiles.edge_radius * 4/4)
        #self.height = int(HexTiles.edge_radius* 4/4)
        self.width = int(player_object.control_board_object.width * 1/7)
        self.height = int(player_object.control_board_object.height * 1/7)
        
        #[type,image_name,tier,cost,code,description]
        self.planet_litc = [['pl',"P_01_01.jpg",1,3,1,"Plnt Dmg +10"],
                            ['pl',"P_01_02.jpg",2,5,2,"Plnt Dmg +10"],
                            ['pl',"P_01_03.jpg",3,7,3,"Plnt Dmg +20"],
                            ['pl',"P_02_01.jpg",1,3,4,"Plnt Hlth +50"],
                            ['pl',"P_02_02.jpg",2,5,5,"Plnt Hlth +50"],
                            ['pl',"P_02_03.jpg",3,7,6,"Plnt Hlth +50"]]
        self.ship_litc = [['sh',"S_01_01.jpg",1,3,1,"Ship Dmg +10"],
                          ['sh',"S_01_02.jpg",2,5,2,"Ship Dmg +10"],
                          ['sh',"S_01_03.jpg",3,7,3,"Ship Dmg +10"],
                          ['sh',"S_02_01.jpg",1,3,4,"Ship Hlth +50"],
                          ['sh',"S_02_02.jpg",2,5,5,"Ship Hlth +50"],
                          ['sh',"S_02_03.jpg",3,7,6,"Ship Hlth +50"],
                          ['sh',"S_03_01.jpg",1,3,7,"Ship Scan +1"],
                          ['sh',"S_04_01.jpg",1,3,8,"Ship Rgen +5"],
                          ['sh',"S_04_02.jpg",2,5,9,"Ship Rgen +5"],
                          ['sh',"S_04_03.jpg",3,7,10,"Ship Rgen +5"],
                          ['sh',"S_05_03.jpg",3,7,11,"Ship FireRng +1"],
                          ['sh',"S_06_02.jpg",2,9,12,"Ship MoveRng +1"]]
        self.random_litc = [['ra',"X_07_01.jpg",1,3,1,"Plsma Rst +10"],
                            ['ra',"X_07_02.jpg",2,5,2,"Plsma Rst +10"],
                            ['ra',"X_07_03.jpg",3,9,3,"Plsma Rst +20"]]
        self.resource_litc = [['re',"R_08_01.jpg",1,3,1,"Sci Mod +1"],
                              ['re',"R_08_02.jpg",2,5,2,"Sci Mod +1"],
                              ['re',"R_08_03.jpg",3,7,3,"Sci Mod +1"],
                              ['re',"R_09_01.jpg",1,3,4,"Prd Mod +1"],
                              ['re',"R_09_02.jpg",2,5,5,"Prd Mod +1"],
                              ['re',"R_09_03.jpg",3,7,6,"Prd Mod +1"]]
        
        self.all_techs_list = [self.planet_litc, self.ship_litc, self.random_litc, self.resource_litc]
        
        #attach cost to description of tech
        for tech_type in self.all_techs_list:
            for tech in tech_type:
                tech[5] = tech[5] + " (" +str(tech[3]) + " Sci)"
        
        self.p_s_ra_re_tier = [1,1,1,1]
        
        self.owned_tech = []
        self.available_tech = []
        
        self.font_type = pygame.font.SysFont("monospace", 14)
        #self.refresh_available_tech()
        #image = pygame.transform.scale(pygame.image.load(os.path.join("images", "tech", self.........)),(GameBoard.width,GameBoard.height))
        
    def grab_random_tech(self):
        self.refresh_available_tech()
        self.random_tech = random.sample(self.available_tech,min(len(self.available_tech),3))
        return self.random_tech
    
    def draw_random_tech(self, screen, xy_list):
        for i , xy in enumerate(xy_list):
            if self.random_tech and len(self.random_tech)-1 >=i:
                self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "tech", self.random_tech[i][1])),(self.width,self.height))
                screen.blit(self.image, (xy[0] - int(self.width)/2, xy[1] - int(self.height)/2))
                self.text = self.font_type.render(self.random_tech[i][5], 1, (255,255,255))
                screen.blit(self.text, (int(xy[0] +self.width/2 + 1), int(xy[1] - self.width/2)) )
                
    def refresh_available_tech(self):
        self.available_tech = []
        for i, tech_type in enumerate(self.all_techs_list):
            for tech in tech_type:
                if tech[2] <= self.p_s_ra_re_tier[i] and tech not in self.owned_tech:
                    self.available_tech.append(tech)
        return self.available_tech
    
    def purchase_tech(self,rand_tech_num):
        self.owned_tech.append(self.random_tech[rand_tech_num])
        if self.random_tech[rand_tech_num][2] == 1:
            pygame.mixer.music.load(os.path.join("audio", "buyTech1.mp3"))
            pygame.mixer.music.play()
        elif self.random_tech[rand_tech_num][2] == 2:
            pygame.mixer.music.load(os.path.join("audio", "buyTech2.wav"))
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load(os.path.join("audio", "buyTech3.wav"))
            pygame.mixer.music.play()
        # update maximum tiers
        for i , tech_type in enumerate(self.all_techs_list):
            if self.random_tech[rand_tech_num] in tech_type and self.random_tech[rand_tech_num][2] >= self.p_s_ra_re_tier[i]:
                self.p_s_ra_re_tier[i] = self.p_s_ra_re_tier[i] + 1
            
        #deduct cost
        self.player_object.sci_resource -= self.random_tech[rand_tech_num][3]
        self.player_object.sci_resource -= 1
        
        #process tech abilities
        if self.random_tech[rand_tech_num][0] == 'pl':
            if self.random_tech[rand_tech_num][4] == 1:
                self.player_object.planet_damage +=10
                for planet in self.player_object.planets_list:
                    planet.damage +=10
            elif self.random_tech[rand_tech_num][4] == 2:
                self.player_object.planet_damage +=10
                for planet in self.player_object.planets_list:
                    planet.damage +=10
            elif self.random_tech[rand_tech_num][4] == 3:
                self.player_object.planet_damage +=20
                for planet in self.player_object.planets_list:
                    planet.damage +=20
            elif self.random_tech[rand_tech_num][4] == 4:
                self.player_object.planet_max_health +=50
                for planet in self.player_object.planets_list:
                    planet.max_health +=50
            elif self.random_tech[rand_tech_num][4] == 5:
                self.player_object.planet_max_health +=50
                for planet in self.player_object.planets_list:
                    planet.max_health +=50
            elif self.random_tech[rand_tech_num][4] == 6:
                self.player_object.planet_max_health +=50
                for planet in self.player_object.planets_list:
                    planet.max_health +=50
        
        elif self.random_tech[rand_tech_num][0] == 'sh':
            if self.random_tech[rand_tech_num][4]== 1:
                self.player_object.ship_damage += 10
            elif self.random_tech[rand_tech_num][4] == 2:
                self.player_object.ship_damage += 10
            elif self.random_tech[rand_tech_num][4] == 3:
                self.player_object.ship_damage += 10
            elif self.random_tech[rand_tech_num][4] == 4:
                self.player_object.ship_max_health += 50
            elif self.random_tech[rand_tech_num][4] == 5:
                self.player_object.ship_max_health += 50
            elif self.random_tech[rand_tech_num][4] == 6:
                self.player_object.ship_max_health += 50
            elif self.random_tech[rand_tech_num][4] == 7:
                self.player_object.ship_scan_range += 1
            elif self.random_tech[rand_tech_num][4] == 8:
                self.player_object.ship_health_regen_rate += 5
            elif self.random_tech[rand_tech_num][4] == 9:
                self.player_object.ship_health_regen_rate += 5
            elif self.random_tech[rand_tech_num][4] == 10:
                self.player_object.ship_health_regen_rate += 5
            elif self.random_tech[rand_tech_num][4] == 11:
                self.player_object.ship_fire_range += 1
            elif self.random_tech[rand_tech_num][4] == 12:
                self.player_object.ship_speed += 1
        
        elif self.random_tech[rand_tech_num][0] == 'ra':
            if self.random_tech[rand_tech_num][4] == 1:
                self.player_object.plasma_defence += 10
                for planet in self.player_object.planets_list:
                    planet.plasma_defence = self.player_object.plasma_defence
            elif self.random_tech[rand_tech_num][4] == 2:
                self.player_object.plasma_defence += 20
                for planet in self.player_object.planets_list:
                    planet.plasma_defence = self.player_object.plasma_defence
            elif self.random_tech[rand_tech_num][4] == 3:
                self.player_object.plasma_defence += 40
                for planet in self.player_object.planets_list:
                    planet.plasma_defence = self.player_object.plasma_defence
        
        elif self.random_tech[rand_tech_num][0] == 're':
            if self.random_tech[rand_tech_num][4] == 1:
                self.player_object.sci_resource_modifier += 1
            elif self.random_tech[rand_tech_num][4] == 2:
                self.player_object.sci_resource_modifier += 1
            elif self.random_tech[rand_tech_num][4] == 3:
                self.player_object.sci_resource_modifier += 1
            elif self.random_tech[rand_tech_num][4] == 4:
                self.player_object.prd_resource_modifier += 1
            elif self.random_tech[rand_tech_num][4] == 5:
                self.player_object.prd_resource_modifier += 1
            elif self.random_tech[rand_tech_num][4] == 6:
                self.player_object.prd_resource_modifier += 1
        

class PlasmaStorms:
    instances_list = []
    storm_counter = 0
    
    @classmethod
    def randomly_generate_storms(cls, HexTiles, turn_counter):
        if turn_counter > 4:
            cls.plasma_storm = PlasmaStorms(HexTiles, random.choice(HexTiles.instances_list), turn_counter)
            return cls.plasma_storm
    
    def __init__(self, HexTiles, hex_object, turn_counter):
        self.instances_list.append(self)
        PlasmaStorms.storm_counter += 1
        
        self.storm_num = PlasmaStorms.storm_counter
        self.hex_object = hex_object
        self.visible = 1
        self.turn_counter = turn_counter
        
        #determine grade of storm based on turn_counter
        if self.turn_counter <12:
            self.grade = 1
        elif self.turn_counter <20:
            self.grade = random.randint(1, 2)
        else:
            self.grade = random.randint(1, 3)
        
        if self.grade == 3:
            self.image = 'X_07_03.jpg'
            self.damage = 70
            self.duration = random.randint(6,9+int(self.turn_counter/4))
        elif self.grade == 2:
            self.image = 'X_07_02.jpg'
            self.damage = 30
            self.duration = random.randint(4,5)
        else:
            self.image = 'X_07_01.jpg'
            self.damage = 10
            self.duration = random.randint(2,3)
        
        self.width = int(HexTiles.edge_radius/2)
        self.height = int(HexTiles.edge_radius/2)
        self.sprite = pygame.transform.scale(pygame.image.load(os.path.join("images", "tech", self.image)),(self.width,self.height))
        
    def draw_storm(self, screen):
        if self.visible == 1:
            screen.blit(self.sprite, (self.hex_object.xy[0] - int(self.width)/2, self.hex_object.xy[1] - int(self.height)/2))
        
    def damage_enemy_ships(self,Ships):
        for enemy_ship in Ships.instances_list:
            # is the ship out of range?
            if enemy_ship.hex_object.xxyyzz != self.hex_object.xxyyzz:
                continue
            enemy_ship.health -= max(int(self.damage * random.uniform(0, 1) - enemy_ship.plasma_defence), 0)
    
    def downgrade_storm(self):
        self.duration -= 1
        # if the storm is finished, delete it; otherwise update damage, and image
        if self.duration <= 0:
            self.damage = 0
            self.visible = 0
            self.grade = 0
            for x , storm in enumerate(PlasmaStorms.instances_list):
                if storm.storm_num == self.storm_num:
                    del PlasmaStorms.instances_list[x]
        elif self.duration < 4:
            self.image = 'X_07_01.jpg'
            self.damage = 10
            self.sprite = pygame.transform.scale(pygame.image.load(os.path.join("images", "tech", self.image)),(self.width,self.height))
        elif self.duration < 6:
            self.image = 'X_07_02.jpg'
            self.damage = 20
            self.sprite = pygame.transform.scale(pygame.image.load(os.path.join("images", "tech", self.image)),(self.width,self.height))
            

        
        
        
        
