_comppll()
{
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    subcommands_1="set del get_all_a get_zones" #возможные подкоманды первого уровня
    subcommands_txt_or_a="A TXT"
    subcommands_maindomain="yourdomain.com"      #возможные подкоманды для history
    subcommands_subdomain="xxxx.yourdomain.com"   #возможные подкоманды для history
    a_or_txt_or_any="A TXT"    #возможные подкоманды для history
    subcommands_ipaddr="ip-address"        #возможные подкоманды для history
    subcommands_txt_text="TXT-text"        #возможные подкоманды для history
    
    
    if [[ ${COMP_CWORD} == 1 ]] ; then # цикл определения автодополнения при вводе подкоманды первого уровня
        COMPREPLY=( $(compgen -W "${subcommands_1}" -- ${cur}) )
        return 0
    fi
    
    
    subcmd_1="${COMP_WORDS[1]}" #К данному моменту подкоманда первого уровня уже введена, и мы её выбираем в эту переменную
    case "${subcmd_1}" in #Дальше смотри, что она из себя представляет

    get_zones)
        COMPREPLY=() #ничего дальше вводить не надо
        return 0
        ;;

    get_all_a)
        if [[ ${COMP_CWORD} == 2 ]] ; then #введены script history; надо подставить import или export
            COMPREPLY=( $(compgen -W "${subcommands_maindomain}" -- ${cur}) )
            return 0
        fi
        subcmd_2="${COMP_WORDS[2]}"
        return 0
        ;;



    set)
        if [[ ${COMP_CWORD} == 2 ]] ; then # цикл определения автодополнения при вводе подкоманды первого уровня
            COMPREPLY=( $(compgen -W "${subcommands_txt_or_a}" -- ${cur}) )
            return 0
        fi
        subcmd_4="${COMP_WORDS[2]}" #К данному моменту подкоманда первого уровня уже введена, и мы её выбираем в эту переменную
        case "${subcmd_4}" in #Дальше смотри, что она из себя представляет
        TXT)
            if [[ ${COMP_CWORD} == 2 ]] ; then #введены script history; надо подставить import или export
                COMPREPLY=( $(compgen -W "${a_or_txt_or_any}" -- ${cur}) )
                return 0
            fi
            subcmd_2="${COMP_WORDS[2]}"

            if [[ ${COMP_CWORD} == 3 ]] ; then #но в любом случае следующим аргументом идет имя проекта.
                COMPREPLY=( $(compgen -W "${subcommands_subdomain}" -- ${cur}) )
                return 0
            fi
            
            if [[ ${COMP_CWORD} == 4 ]] ; then #но в любом случае следующим аргументом идет имя проекта.
                COMPREPLY=( $(compgen -W "${subcommands_txt_text}" -- ${cur}) )
                return 0
            fi

            ;;
        A)
            if [[ ${COMP_CWORD} == 2 ]] ; then #введены script history; надо подставить import или export
                COMPREPLY=( $(compgen -W "${a_or_txt_or_any}" -- ${cur}) )
                return 0
            fi
            subcmd_2="${COMP_WORDS[2]}"

            if [[ ${COMP_CWORD} == 3 ]] ; then #но в любом случае следующим аргументом идет имя проекта.
                COMPREPLY=( $(compgen -W "${subcommands_subdomain}" -- ${cur}) )
                return 0
            fi
            
            if [[ ${COMP_CWORD} == 4 ]] ; then #но в любом случае следующим аргументом идет имя проекта.
                COMPREPLY=( $(compgen -W "${subcommands_ipaddr}" -- ${cur}) )
                return 0
            fi

            ;;
        esac
        return 0
        ;; 

    del) 
        if [[ ${COMP_CWORD} == 2 ]] ; then #введены script history; надо подставить import или export
            COMPREPLY=( $(compgen -W "${a_or_txt_or_any}" -- ${cur}) )
            return 0
        fi
        subcmd_2="${COMP_WORDS[2]}"

        if [[ ${COMP_CWORD} == 3 ]] ; then #но в любом случае следующим аргументом идет имя проекта.
            COMPREPLY=( $(compgen -W "${subcommands_subdomain}" -- ${cur}) )
            return 0
        fi
        ;;
    esac

    return 0
    
}
complete -F _comppll dns

