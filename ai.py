import libtcodpy as libtcod
import math
import textwrap

class BasicMonster:
	#AI for a basic monster.
	def __init__(self):
		self.recharge_time = 0
		self.stunned_time = 0

	def decide(self):
		#a basic monster takes its turn. If you can see it, it can see you
		decider = self.owner
		monster = decider.owner #yaaay
		# only do thing (including weapon recharge? maybe not) if not stunned
		if self.stunned_time <= 0:
			if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
	
				#move towards player if far away
				if monster.distance_to(player) >= 2:
					(dx,dy) = next_step_towards(monster.x, monster.y, player.x, player.y)
					# only walk if there's not something in the way. controversial maybe!
					if is_blocked(monster.x+dx, monster.y+dy) == False:
						decider.decision = Decision(move_decision=Move_Decision(dx,dy))
 	
				#close enough, attack! (if the player is still alive.)
				elif player.fighter.hp > 0 and self.recharge_time <= 0:
					attackList = []
	
					(dx,dy) = next_step_towards(monster.x, monster.y, player.x, player.y)
					attack_component = BasicAttack(damage=1,lifespan=1, attacker=monster)
					attack = Object(monster.x+dx, monster.y+dy, '#', 'monAttack', libtcod.dark_red, blocks=False, attack=attack_component)
					attackList.append(attack)
					decider.decision = Decision(attack_decision=Attack_Decision(attackList))
					self.recharge_time = 2
					#monster.fighter.attack(player)
		
			if self.recharge_time > 0:
				self.recharge_time = self.recharge_time - 1
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1

	def stun(self):
		self.stunned_time = 2
