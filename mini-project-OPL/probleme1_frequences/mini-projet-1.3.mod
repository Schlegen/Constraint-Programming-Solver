/*********************************************
 * OPL 12.10.0.0 Model
 * Author: maxime
 * Creation Date: 13 d�c. 2021 at 14:59:29
 *********************************************/

using CP;

// Definition des donn�es du probl�mes
int nb_emetteurs = 7;
int valeurMax = 10;

range valeurs = 1..valeurMax;
range emetteurs = 1..nb_emetteurs;

// Definition de l'offset
tuple offset {
  int emett1;
  int emett2;
  int value;
}

{offset} offsets = ...;

dvar int freq[emetteurs] in valeurs;

// Variable auxiliaire pour d�finir le max
dvar int freq_max in valeurs;

// Contraintes

// maximize freq_max;

constraints {
	// Toutes les frequences sont differentes
   	// allDifferent(all (i in emetteurs) freq[i]);
   	
   	 // Definition du max
   	forall (i in emetteurs){
   	  freq_max >= freq[i];
 	}
 
 	ctMaxValue: freq_max <= valeurMax; 
 	
 	// Contraintes d'offset
 	forall (o in offsets){
 	  abs(freq[o.emett1] - freq[o.emett2]) >= o.value;
 	}
 	
 	forall (i in emetteurs){
 	  i mod 2 == freq[i] mod 2;
 	}
 	
}; 

// Main block
 main {
	thisOplModel.generate();

	var N1 = 10;

	while (cp.solve()) {
		N1 = thisOplModel.freq_max;

		write("solution de frequence max " + N1 + " : [");
		for (var i in thisOplModel.freq)
			write(thisOplModel.freq[i]+ ",");
		writeln("]");
 		
 		//mise à jour de la borne supérieure
 		thisOplModel.freq_max.UB = N1-1;
	}
} 