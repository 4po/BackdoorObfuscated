# BackdoorObfuscated
Backdoor Obfuscated Macro ( Cachée ) Développé par 4po.

Clause de non-responsabilité : Conçu pour l'expérience de codage et pour tester les mesures de sécurité du client dans le cadre de ses missions. NE PAS utiliser contre des systèmes/utilisateurs sur lesquels vous n'avez pas la permission explicite de faire des tests.

Il s'agit d'un vecteur d'attaque en deux étapes, la macro initiale qu'un utilisateur exécute configurera des raccourcis ciblés sur son bureau pour exécuter un stager powerhell. La deuxième étape se produit lorsque l'utilisateur clique sur le raccourci, le talon de téléchargement de powerhell qui s'exécute ouvrira d'abord l'exécutable cible, puis nettoiera tous les raccourcis cachés sur le bureau de l'utilisateur, et enfin tentera de télécharger et d'exécuter le code de lancement d'empire à partir d'un fichier xml hébergé sur un serveur web prédéfini. Ce fichier xml contient un lanceur d'empire complet, qui sera téléchargé et exécuté en mémoire, ce qui rendra à son tour une coquille d'empire complète. Le XML est téléchargé en utilisant la méthode XmlDocument.Load car il est intrinsèquement compatible avec les proxy et permet un téléchargement propre du code du lanceur.

Lors de l'exécution, la macro recherchera sur le bureau de l'utilisateur tous les fichiers .lnk (raccourcis) qui correspondent aux exécutables cibles tels que définis lors de la génération de la macro. Les cas d'utilisation typiques se concentrent sur des raccourcis très utilisés (iexplore, chrome, firefox, etc.)

L'approche en deux étapes vise à déjouer les mesures de sécurité liées aux applications qui signalent le lancement de powerhell à partir de programmes inattendus, comme un lancement direct à partir d'applications de bureau. Comme la macro est purement VBA et n'exploite pas powerhell ou n'engendre aucun processus enfant, elle a moins de chances d'être détectée par ce type d'outils. En outre, les modifications apportées par la macro ne devraient pas nécessiter de droits administratifs sur le point final. L'obscurcissement de la macro est effectué pour éviter les virus. La macro est actuellement configurée comme une Auto_Close() pour une évasion de base du bac à sable, n'hésitez pas à changer de méthode d'exécution si nécessaire.

Utilisation : Déposez backdoorLnkMacroObfuscated.py dans rootEmpireFolder/lib/stagers/windows et start empire,  le stager devrait maintenant apparaître dans votre liste (usestager windows/backdoorLnkMacroObfuscated.py)

Lors de l'exécution du stager, un fichier macro et un fichier xml seront générés, assurez-vous que le xml se trouve sur le serveur web configuré lors de l'installation du stager et qu'il s'agit d'un emplacement accessible sur le système distant.

Créé par 4po (apo#0001)
