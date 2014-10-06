(defproblem hanoi-10 hanoi-domain
	(
	 (disk d1) (size d1 1)
	 (disk d2) (size d2 2)
	 (disk d3) (size d3 3)
	 (disk d4) (size d4 4)
	 (disk d5) (size d5 5)
	 (disk d6) (size d6 6)
	 (disk d7) (size d7 7)
	 (disk d8) (size d8 8)
	 (disk d9) (size d9 9)
	 (disk d10) (size d10 10)
	 (peg p1) (size p1 11) 
	 (peg p2) (size p2 11) 
	 (peg p3) (size p3 11)
	 
	 (top p1 p1) (top p2 p2) (top p3 p3)
	 
	 (on d1 d2) (on d2 d3) (on d3 d4) (on d4 d5) (on d5 d6) (on d6 d7) (on d7 d8) (on d8 d9) (on d9 d10) (on d10 p3)
	)
	(:unordered (:task (hanoi-sub d10 p3 p1 p2)))
)