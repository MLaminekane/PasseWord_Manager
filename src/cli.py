import argparse
import getpass
import sys
from datetime import datetime
from database import init_db, register_user, verify_user, add_password, get_password

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════╗
║         -GESTIONNAIRE DE MOTS DE PASSE       ║
║         -PASSEWORD MANAGER                   ║
╚══════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_password(label, password):
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}🔐 Mot de passe trouvé :{Colors.END}")
    print(f"{Colors.CYAN}Label: {Colors.BOLD}{label}{Colors.END}")
    print(f"{Colors.GREEN}Mot de passe: {Colors.BOLD}{password}{Colors.END}\n")

def print_usage():
    usage = f"""
{Colors.YELLOW}{Colors.BOLD}UTILISATION:{Colors.END}

{Colors.CYAN}Inscription:{Colors.END}
  {Colors.WHITE}python main.py -r {Colors.BOLD}username{Colors.END}

{Colors.CYAN}Ajouter un mot de passe pour un Label:{Colors.END}
  {Colors.WHITE}python main.py -u {Colors.BOLD}username{Colors.END} -a {Colors.BOLD}label mot_de_passe{Colors.END}

{Colors.CYAN}Afficher le mot de passe associé à un label quelconque:{Colors.END}
  {Colors.WHITE}python main.py -u {Colors.BOLD}username{Colors.END} -s {Colors.BOLD}label{Colors.END}

{Colors.CYAN}Exemples:{Colors.END}
  {Colors.WHITE}python main.py -r john{Colors.END}
  {Colors.WHITE}python main.py -u john -a email MonSuperPass123{Colors.END}
  {Colors.WHITE}python main.py -u john -s email{Colors.END}
"""
    print(usage)

def main():
    print_banner()
    init_db()
    
    parser = argparse.ArgumentParser(description='Password Manager - Gestion sécurisée des mots de passe', add_help=False)
    
    parser.add_argument('-r', '--register', metavar='USERNAME', help='Inscrire un nouvel utilisateur')
    parser.add_argument('-u', '--user', metavar='USERNAME', help="Nom d'utilisateur pour les opérations")
    parser.add_argument('-a', '--add', nargs=2, metavar=('LABEL', 'PASSWORD'), help='Ajouter un mot de passe: -a label mot_de_passe')
    parser.add_argument('-s', '--show', metavar='LABEL', help='Afficher un mot de passe: -s label')
    parser.add_argument('-h', '--help', action='store_true', help="Afficher ce message d'aide")
    
    args = parser.parse_args()
    
    # Aide
    if args.help or len(sys.argv) == 1:
        print_usage()
        return
    
    # Mode inscription
    if args.register:
        print(f"\n{Colors.CYAN}{Colors.BOLD}📝 INSCRIPTION NOUVEL UTILISATEUR{Colors.END}")
        print(f"{Colors.WHITE}Utilisateur: {Colors.BOLD}{args.register}{Colors.END}")
        master_password = getpass.getpass(f'{Colors.YELLOW}🔒 Entrez le master password pour {args.register}: {Colors.END}')
        
        if register_user(args.register, master_password):
            print_success(f"Utilisateur {args.register} inscrit avec succès!")
        else:
            print_error("Erreur: Cet utilisateur existe déjà!")
    
    # Mode ajout de mot de passe
    elif args.user and args.add:
        print(f"\n{Colors.CYAN}{Colors.BOLD}➕ AJOUT D'UN MOT DE PASSE{Colors.END}")
        print(f"{Colors.WHITE}Utilisateur: {Colors.BOLD}{args.user}{Colors.END}")
        label, password = args.add
        print(f"{Colors.WHITE}Label: {Colors.BOLD}{label}{Colors.END}")
        
        master_password = getpass.getpass(f'{Colors.YELLOW}🔒 Entrez le master password pour {args.user}: {Colors.END}')
        
        if verify_user(args.user, master_password):
            if add_password(args.user, label, password, master_password):
                print_success(f"Mot de passe '{label}' sauvegardé avec succès!")
            else:
                print_error("Erreur: Impossible de sauvegarder le mot de passe (label peut-être déjà utilisé)!")
        else:
            print_error("Erreur: Master password invalide ou utilisateur non trouvé!")
    
    # Mode affichage de mot de passe
    elif args.user and args.show:
        print(f"\n{Colors.CYAN}{Colors.BOLD}🔍 RECHERCHE DE MOT DE PASSE{Colors.END}")
        print(f"{Colors.WHITE}Utilisateur: {Colors.BOLD}{args.user}{Colors.END}")
        print(f"{Colors.WHITE}Label: {Colors.BOLD}{args.show}{Colors.END}")
        
        master_password = getpass.getpass(f'{Colors.YELLOW}🔒 Entrez le master password pour {args.user}: {Colors.END}')
        
        if verify_user(args.user, master_password):
            password = get_password(args.user, args.show, master_password)
            if password:
                print_password(args.show, password)
            else:
                print_error("Erreur: Aucun mot de passe trouvé pour ce label!")
        else:
            print_error("Erreur: Master password invalide ou utilisateur non trouvé!")
    
    else:
        print_error("Commande invalide!")
        print_usage()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Arrêt du programme. Au revoir!{Colors.END}")
    except Exception as e:
        print_error(f"Erreur inattendue: {str(e)}")