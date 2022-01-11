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



//// Gestion de la parite 2
// int semiValMax = valeurMax div 2;
//{int} emetteurs_pairs  = {2,4,6};
//{int} emetteurs_impairs = {1,3,5,7};
//range semi_valeurs = 1..semiValMax;

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

// Objectif
//minimize freq_max;

// Contraintes
constraints {
 
	// Toutes les frequences sont differentes
   	// allDifferent(all (i in emetteurs) freq[i]);
   	
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

 	// Contraintes de parité 2
// 	forall (i in emetteurs_pairs){
// 	  freq[i] == 2 * semi_freq[i];
// 	}
// 	forall (i in emetteurs_impairs){
// 	  freq[i] == 2 * semi_freq[i] - 1;
// 	}
// 	
};

// Main block
 main {
	thisOplModel.generate();
	
	var n    = 0;
	var nMax = 9;
	
	var N0 = 10;
	N0 = cp.getObjValue();
	
	cp.param.SearchType="MultiPoint";
	//cp.param.Workers=1;
	
	cp.startNewSearch();
	while (cp.next() && n<=nMax) {
		n++;
		write("solution " + n + " [");
		for (var i in thisOplModel.freq)
			write(thisOplModel.freq[i]+ ",");
		writeln("]");
	}
} 