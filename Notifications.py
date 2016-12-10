
class Notifications:
	SUM_OF_OPPOSITE_SIDES = 7

	# Improper input error msg
	def msg_improper_input(self):
		print "\nERROR:\t\t Why you annoying me with improper inputs? Go, Try again!\n"

	# Enter move origin's row
	def msg_enter_origin_row(self):
		print "\nEnter the ROW of the dice you want to move :- "
	
	# Enter move origin's column
	def msg_enter_origin_column(self):
		print "\nEnter the COLUMN of the dice you want to move :- "

	# Enter destination row
	def msg_enter_destination_row(self):
		print "\nEnter the ROW of the destination :- "

	# Enter destination column
	def msg_enter_destination_column(self):
		print "\nEnter the COLUMN of the destination :- "

	# Input out of bounds error msg
	def msg_input_out_of_bounds(self):
		print "\nERROR:\t\t Input co-ordinates out of bound. *Rolls eyes* Try again!\n"
	
	# Moving another player's dice error msg
	def msg_wrong_dice(self):
		print "\nERROR:\t\t Woah! Foul! That ain't your dice to move homie!\n"
	
	# No dice to move error msg
	def msg_no_dice_to_move(self):
		print "\nERROR:\t\t Don't you see there is no dice to move in that co-ordinate?\n"
	
	# Invalid move error msg
	def msg_invalid_move(self):
		print "\nERROR:\t\t Why you always trying Invalid Moves?\n"
	
	# Trying to run own dice error msg
	def msg_running_over_own_dice(self):
		print "\nMSG:\t\t Are you really trying to capture your own dice, bonehead?\n"

	# Captured opponent msg
	def msg_captured_an_opponent(self):
		print "\nMSG:\t\t You just captured an opponent dice. Impressive for a Knucklehead? Eh!\n"

	# No valid path msg
	def msg_no_valid_path(self):
		print "\nERROR:\t\t Yo numskull! NO Valid Path was found to get to your selected destination. BOOO!\n"
	
	# Enter path choice for 90 degree turns prompt
	def msg_90degree_path_selection(self):
		print "\n90 Degree turn detected. Enter 1 to go vertically first, or 2 to go laterally first :- "
	
	# 90 degree turns re-routed msg
	def msg_90degree_path_selection_not_processed(self):
		print "\nMSG:\t\t We're sorry, but your DUMB path selection for the 90 Degree turn was Invalid.\n"
		print "\t\t So, we - the smart bots species - automatically chose the alternate route for you.\n"
	
	# Nature of path taken msg
	def msg_nature_of_path_taken(self, path):
		print "\nMSG:\t\t A %s path was taken to get to the destination\n" %(path)	

	# Displaying start and end coordinates of the move
	def msg_move_description(self, startRow, startCol, endRow, endCol, topValueAtStart, rightValueAtStart, topValueAtEnd, rightValueAtEnd, botOperated):
		player = 'C' if botOperated else 'H'
		rightValueAtStart = self.SUM_OF_OPPOSITE_SIDES - rightValueAtStart if botOperated else rightValueAtStart
		rightValueAtEnd = self.SUM_OF_OPPOSITE_SIDES - rightValueAtEnd if botOperated else rightValueAtEnd

		print "ACTION:\t\t The dice %s%s%s in (%s,%s) was moved to (%s,%s). It is now %s%s%s \n" %(player, topValueAtStart, rightValueAtStart, startRow, startCol, endRow, endCol, player, topValueAtEnd, rightValueAtEnd)
		print "\t\t There were %s vertical rolls & %s horizontal rolls made.\n" %(abs(startRow - endRow), abs(startCol - endCol))

	# Crash msg
	def msg_crashed_while_making_the_move(self):
		print "\nERROR:\t\t Whoopsie Daisy! The program crashed while making the move.\n"
	
	# Displays toss results
	def msg_toss_results(self, winner, humanToss, computerToss):
		print "TOSS RESULTS\nHuman:\t\t%s\nComputer:\t%s\n" %(humanToss, computerToss)
		print "MSG:\t\t%s won the toss!\n" %(winner)

	# Displays the turns
	def msg_turns(self, player):
		print "\n"
		print "***************************************************************\n"
		print "\t\t%s\n" %(player)
		print "***************************************************************\n"	

	# Displays results of the tournament
	def msg_display_results(self, botScore, humanScore):
		print "***************************************************************\n"
		print "\t\tTournament Results\n"
		print "***************************************************************\n"
		print "Computer Wins:	%s\n"  %(botScore)
		print "Human Wins: %s\n"  %(humanScore)
		if (botScore > humanScore):
			print "The Computer Won the Tournament. *reinforcing the notion once again that we bots are better than you humans*\n"
		elif (humanScore > botScore):
			print "Congratulations! You won the Tournament. Our programmer must've done a terrible job on algorithms for someone like you to win.\n"
		else:
			print "It was a draw. Guess we'll see who's better in the next tournament.\n"

	# Prompt to ask user if they want to play again
	def msg_want_to_play_again(self):
		print "\nMSG:\t Do you want to play another round? (y or n)? "	

	# Draws a divider line
	def draw_divider(self):
		print "\n\n-*-*-*-*-********************************************-*-*-*-*-\n\n"
		
	# Notifying the game is over
	def msg_game_over(self, winner):
		print "\n-*-*-*-*-**********%s WON**********************************-*-*-*-*-\n" %(winner)
	
	# Prompt msg to serialize
	def msg_serialize_prompt(self):
		print "\nWant to Serialize? Press 'y' to serialize, 'n' to continue :- "

	# Prompt to ask user if they want help mode on
	def msg_help_mode_prompt(self):
		print "Need Help? Press 'y' to turn help mode ON, 'n' to continue :- "
	
	# Serialization failed and exit
	def msg_serialized(self, status):
		print "\nSerialization %s. The game will exit now.\n" %(status)
		self.draw_divider()

	# User's wish to restore from file
	def msg_restore_from_file(self):
		print "Do you want to restore the tournament from an existing file (y/n)? "

	# Prompt to ask file path
	def msg_enter_file_path(self):
		print "\nEnter a valid file path to restore the tournament :- "

	"""
	THE FOLLOWING FUNCTIONS ARE ESPECIALLY MEANT TO GUIDE THE USER THROUGH COMPUTER'S THOUGHT PROCESS
	"""

	# Bot trying to capture opponent key pieces/squares msg
	def botsthink_trying_to_capture_opponentkeys(self):
		print "Bots Mumbling:\t Trying to capture opponent's King or KeySquare...\n"

	# Msg notifying that the safety of key pieces/squares are being taken care of
	def botsthink_checking_king_keysquare_safety(self):
		print "Bots Mumbling:\t Monitoring territory to ensure the King & KeySquare are safe...\n"
	
	# Key Threat detected msg
	def botsthink_keythreat_detected(self, whosUnderThreat):
		print "Bots Mumbling:\t Imminent threat has been detected for the %s\n" %(whosUnderThreat)

	# hostile opponent captured msg
	def botsthink_hostile_opponent_captured(self, whosUnderThreat):
		print "Bots Mumbling:\t That hostile opponent aiming to attack our %s has been captured.\n" %(whosUnderThreat)

	# hostile opponent not capturable msg
	def botsthink_hostile_opponent_uncapturable(self, whosUnderThreat):
		print "Bots Mumbling:\t That hostile opponent aiming to attack the %s couldn't be captured. Trying alternatives...\n" %(whosUnderThreat)	

	# Blocking move successful msg
	def botsthink_blocking_move_made(self):
		print "Bots Mumbling:\t A Blocking move was successfully made to obstruct the hostile opponent.\n"
	
	# Blocking move not successful msg
	def botsthink_blocking_move_not_possible(self):
		print "Bots Mumbling:\t A Blocking move wasn't possible at this time. Trying other options...\n"	

	# King relocation successful msg
	def botsthink_king_moved(self):
		print "Bots Mumbling:\t The king has been moved and the threat has been averted for now.\n"
	
	# King move unsafe msg
	def botsthink_unsafe_to_move_king(self):
		print "Bots Mumbling:\t No safe surroundings to move the king. The humans have trapped our King.\n"
	
	# Trying to capture opponent msg
	def botsthink_trying_to_capture_opponent_dice(self):
		print "Bots Mumbling:\t Looking for any vulnerable opponent dice to capture at this point...\n"
	
	# Captured opponent msg
	def botsthink_captured_opponent_dice(self):
		print "Bots Mumbling:\t We captured an opponent die.\n"

	# Checking to see if any of own dice are threatened by opponent dices
	def botsthink_protect_dices_from_potential_captures(self):
		print "Bots Mumbling:\t Checking if any of the own dices are under threat of being captured by opponent...\n"
	
	# searching an ordinary move msg
	def botsthink_searching_ordinary_move(self):
		print "Bots Mumbling:\t Examining possible moves to get closer to the opponent king/keysquare...\n"
	
	# Help mode on msg
	def msg_helpmode_on(self):
		print "\nHELP MODE ACTIVATED!\n"
	
	# Prints the move recommended by the computer
	def msg_helpmode_recommended_move(self, startRow, startCol, endRow, endCol, pathChoice):
		if pathChoice == 1:
			path = "Vertical then Lateral Path"
		elif pathChoice == 2:
			path = "Lateral then Vertical Path"
		elif pathChoice == 3:
			path = "Vertical Path"
		elif pathChoice == 4:
			path = "Lateral Path"
		else:
			path = "Unknown Path"
		
		print "\nRECOMMENDED:\t Move the dice in square (%s,%s) to (%s,%s) using a %s.\n"  %(startRow, startCol, endRow, endCol, path)
		print "\nHELP MODE DEACTIVATED!\n"