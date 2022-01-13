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
//dvar int semi_freq[emetteurs] in semi_valeurs;

// Variable auxiliaire pour d�finir le max
dvar int freq_max in valeurs;


// Contraintes
constraints {
   	
   	 // Definition du max
   	forall (i in emetteurs){
   	  freq_max >= freq[i];
 	}
 	
 	// Contraintes d'offset
 	forall (o in offsets){
 	  abs(freq[o.emett1] - freq[o.emett2]) >= o.value;
 	}

//	 Contraintes de parité 1
	forall (i in emetteurs){
	  i mod 2 == (freq[i]) mod 2;
	}
};

// Main block
 main {
	thisOplModel.generate();
	
	var n    = 0;
	var nMax = 9;
	
	cp.param.SearchType="MultiPoint";
	
	cp.startNewSearch();
	while (cp.next() && n<=nMax) {
		n++;
		write("solution " + n + " [");
		for (var i in thisOplModel.freq)
			write(thisOplModel.freq[i]+ ",");
		writeln("]");
	}
} 