/* ----------------------- */
/* -------- FACTS -------- */
/* ----------------------- */

singing(elon).
singing(jeff).

playingGuitar(mark).
playingGuitar(satya).

/* ----------------------- */
/* -------- RULES -------- */
/* ----------------------- */

playingGuitar(elon):- happy(elon).

happy(mark):-
	singing(mark),
	playingGuitar(mark).


happy(satya):-
	singing(satya);
	playingGuitar(satya).


sad(satya):-
not(playingGuitar(satya)).

grumpy(jeff):-
	singing(jeff)->
		false;
		true.