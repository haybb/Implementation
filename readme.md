# TIPE - Paradoxe de Braess
  
## Propos
Ceci est mon TIPE réalisé lors de ma 5/2 en MP.  
Le thème de l'année était "la ville".  
J'ai ainsi décidé de modéliser le paradoxe de Braess.  
  

## Explications
Les explications complètes figurent dans **Presentation_TIPE.pdf.**  

**TL;DR** : ce paradoxe montre qu'enlever une route à un traffic congestionné peut en réalité fluidifier ce dernier.  
Pour modéliser ceci, j'ai utilisé des jeux de routage (notamment des graphes à débit),  
et la théorie des jeux, avec entre autres des calculs d'équilibre de Wardrop (situation réelle),  
et d'optimum social (équilibre idéal et théorique).   
La différence entre ces 2 derniers équilibres met notamment en évidence le phénomène.  

Je propose également une solution d'optimisation en instaurant une taxe pigouvienne,  
ie un ralentissement volontaire sur certaines routes (tel que des feux rouges).
  

## Comment exécuter le programme ?
Tout d'abord il faut installer les modules nécessaires : ```pip3 install numpy matplotlib networkx```  
Puis lancer l'implémentation python du modèle : ```python3 TIPE.py```  
  

## Exemple  
  
### Ecart entre l'optimum social et l'équilibre de Wardrop  
Si l'on enlève la route 1->2, le traffic est plus fluide :  
on passe de 3 chemins possibles (0->1->2;  0->1->3->2;  0->3->2) à 2 (0->1->2;  0->3->2), ceci diminuant le coût par arc.
![Ecart équilibres](/Images/accord%20modeles.png "Ecart équilibres")  
  
## Efficacité de la taxe pigouvienne  
Une fois la taxe suffisante, le comportement réel rejoint le comportement théorique souhaité.  
![Variation taxes](/Images/variation%20taxe.png "Variation taxes")  
