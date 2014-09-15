Require Import List.
Require Import ZArith.
Require Import sort. (* roba od Bauerja *)
Require Import Recdef. (* to potrebujemo za definicijo s [Function]. *)

Fixpoint vstavi (x : Z) (l : list Z) :=
  match l with
    | nil => x::nil
    | y::l' => if (Z.leb x y) then x::l else y:: (vstavi x l') 
  end.

Fixpoint insertion( l : list Z) :=
   match l with
    | nil => nil
    | x::l' =>
       let l'' := insertion l' in 
          vstavi x l''
   end.

Lemma urejen_tail (x : Z) (l : list Z) :
  urejen(x::l) -> urejen(l).
Proof.
  induction l;auto.
  intros[? ?].
  auto.
Qed.

Eval compute in insertion (1::4::3::6::2::8::7::nil)%Z.

Lemma vstaviP: forall a : Z, forall l:list Z,
  urejen (l) -> urejen(vstavi a l).
Proof.
  induction l.
  -simpl ; auto.
  -intros.
   simpl.
  (* TODO: SearchAbout za case_eq *) 
   case_eq (Z.leb a a0).
   intros G.
     + simpl.
       destruct l.
         *firstorder.
           apply Zle_is_le_bool.
           assumption.
          *split.
           apply Zle_is_le_bool.
           assumption.
           split.
           unfold urejen in H.
           destruct H.
             assumption.

             apply urejen_tail in H.
             assumption.
     +intro.
      simpl.
      destruct l;simpl.
        *firstorder.
          SearchAbout(?x < ?y -> ?x <= ?y)%Z.
          apply Z.lt_le_incl.
          SearchAbout(?x <=? ?y)%Z.
          assert (G := Zle_cases a a0).
          rewrite H0 in G.
          firstorder.
          *
          (* TODO: Dokoncaj *)


Lemma pravilnost1 (l : list Z):
  urejen (insertion l).
Proof.
induction l.
    -simpl.
     auto.
    -simpl.
