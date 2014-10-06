(in-package :shop2-user)

(defun define-hanoi-domain ()
	(let (( *define-silently* t))
		(defdomain hanoi-domain (
			(:operator (!move-disk ?disk ?below ?new-below ?source ?dest)
				(
				 (disk ?disk) 			;precondition
				 (size ?disk ?sX)
				 (size ?new-below ?sY)
				 (call < sX sY)
				 (on ?disk ?below)
				 (call /= ?below ?new-below)
				 (call /= ?disk ?below)
				 (call /= ?disk ?new-below)
				 (top ?new-below ?dest)
				 (top ?disk ?source)
				)
				(
				 (on ?disk ?below)			;delete list
				 (top ?new-below)
				)
				(
				 (on ?disk ?new-below)		;add list
				 (top ?below)
				)
			)
			
			(:method (movePegDisk ?source ?dest)
				(
				 (peg ?source) (peg ?dest)
				 (top ?sourceDisk ?source) (top ?destDisk ?dest)
				 (on ?sourceDisk ?belowDisk)
				)
				(:ordered (:task move-disk ?sourceDisk ?belowDisk ?destDisk ?source ?dest))
			)
			
			(:method (hanoi-sub ?base-disk ?source ?target ?spare)
				((size ?base-disk ?x)
				 (call > ?x 0)
				 (disk ?base-disk) 
				 (peg ?target) 
				 (peg ?spare)
				 (disk ?aboveDisk) (on ?aboveDisk ?base-disk)
				)
				(:ordered
				 (:task hanoi-sub ?aboveDisk ?source ?spare ?dest)
				 (:task movePegDisk ?source ?dest)
				 (:task hanoi-sub ?aboveDisk ?spare ?dest ?source)
				)
				
				((size ?base-disk ?x)
				 (call <= ?x 0)
				 (disk ?base-disk) 
				 (peg ?target) 
				 (peg ?spare)
				 (disk ?aboveDisk) (on ?aboveDisk ?base-disk)
				)
				(:ordered
				 (:task movePegDisk ?source ?dest)
				)
			)
				 
				
		)
)

(eval-when (:load-toplevel)
  (define-blocks-domain))