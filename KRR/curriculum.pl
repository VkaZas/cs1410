/* ----------------------- */
/* -------- FACTS -------- */
/* ----------------------- */

fall(cs15).
fall(cs17).
fall(cs33).
fall(cs141).
fall(cs126).

spring(cs16).
spring(cs18).
spring(cs22).
spring(cs32).
spring(cs166).

has_prereqs(cs16, cs15).
has_prereqs(cs18, cs17).
has_prereqs(cs141, cs22).
has_prereqs(cs141, cs18).
has_prereqs(cs141, cs16).
has_prereqs(cs126, cs22).
has_prereqs(cs126, cs32).
has_prereqs(cs33, cs16).
has_prereqs(cs33, cs18).
has_prereqs(cs32, cs16).
has_prereqs(cs32, cs18).
has_prereqs(cs166, cs33).

strong_prereqs(cs141, cs22).
strong_prereqs(cs16, cs15).
strong_prereqs(cs18, cs17).
strong_prereqs(cs126, cs22).
strong_prereqs(cs126, cs32).
strong_prereqs(cs166, cs33).

weak_prereqs(cs141, cs16).
weak_prereqs(cs141, cs18).
weak_prereqs(cs32, cs16).
weak_prereqs(cs32, cs18).
weak_prereqs(cs33, cs16).
weak_prereqs(cs33, cs18).

no_prereqs(cs15).
no_prereqs(cs22).
no_prereqs(cs17).

no_strong_prereqs(cs15).
no_strong_prereqs(cs17).
no_strong_prereqs(cs33).
no_strong_prereqs(cs32).
no_strong_prereqs(cs22).

no_weak_prereqs(cs15).
no_weak_prereqs(cs17).
no_weak_prereqs(cs16).
no_weak_prereqs(cs18).
no_weak_prereqs(cs22).
no_weak_prereqs(cs126).
no_weak_prereqs(cs166).

has_taken(mark, cs32).
has_taken(mark, cs18).
has_taken(mark, cs16).
has_taken(mark, cs15).
has_taken(mark, cs17).

has_taken(elon, cs17).
has_taken(elon, cs16).
has_taken(elon, cs15).
has_taken(elon, cs22).
has_taken(elon, cs141).
has_taken(elon, cs33).
has_taken(elon, cs166).

has_taken(sheryl, cs33).
has_taken(sheryl, cs32).
has_taken(sheryl, cs22).
has_taken(sheryl, cs18).
has_taken(sheryl, cs17).

has_taken(jeff, cs15).
has_taken(jeff, cs17).
has_taken(jeff, cs22).
has_taken(jeff, cs16).
has_taken(jeff, cs18).
has_taken(jeff, cs141).
has_taken(jeff, cs33).
has_taken(jeff, cs166).


/* ----------------------- */
/* -------- RULES -------- */
/* ----------------------- */

course(Course):-
  fall(Course);
  spring(Course).

% intros: cs15, cs16, cs17, cs18
intro(Course):-
  course(Course),
  fall(Course), no_prereqs(Course);
  spring(Course), has_prereqs(Course, Prereq), no_prereqs(Prereq).

% intermediates: cs32, cs33
intermediate(Course):-
  course(Course),
  not(intro(Course)),
  not(no_prereqs(Course)),
  not((has_prereqs(Course, Prereq), not(intro(Prereq)), !)).

% upper_levels: cs141, cs126, cs166
upper_level(Course):-
  course(Course), not(no_prereqs(Course)), (
    not((has_prereqs(Course, Prereq), intro(Prereq), !));
    has_prereqs(Course, cs22), not(
      (has_prereqs(Course, Prereq2), Prereq2 \== cs22, not(intro(Prereq2)), !)
    )
  ).

can_take(Student, Course):-
  course(Course), (
    no_prereqs(Course);
    (  % STRONG prereqs
      no_strong_prereqs(Course);
      not(
        (strong_prereqs(Course, Y), not(has_taken(Student, Y)), !)
      )
    ),( % WEAK prereqs
      no_weak_prereqs(Course);
      (weak_prereqs(Course, Y), has_taken(Student, Y))
    )
  ),
  (
    (Student \== elon);
    not(has_taken(elon, Course))
  ).
