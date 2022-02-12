_comppll()
{
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    subcommands_1="add del get_all_a get_zones" #возможные подкоманды первого уровня
    subcommands_maindomain="yourdomain.com"      #возможные подкоманды для history
    subcommands_subdomain="xxxx.yourdomain.com"   #возможные подкоманды для history
    subcommands_ipaddr="your_ip_address"        #возможные подкоманды для history
    
    
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
    add)
        if [[ ${COMP_CWORD} == 2 ]] ; then #введены script history; надо подставить import или export
            COMPREPLY=( $(compgen -W "${subcommands_subdomain}" -- ${cur}) )
            return 0
        fi
        subcmd_2="${COMP_WORDS[2]}"

        if [[ ${COMP_CWORD} == 3 ]] ; then #но в любом случае следующим аргументом идет имя проекта.
            COMPREPLY=( $(compgen -W "${subcommands_ipaddr}" -- ${cur}) )
            return 0
        fi
        ;;

    del) 
        if [[ ${COMP_CWORD} == 2 ]] ; then #введены script history; надо подставить import или export
            COMPREPLY=( $(compgen -W "${subcommands_subdomain}" -- ${cur}) )
            return 0
        fi
        subcmd_2="${COMP_WORDS[2]}"
        return 0
        ;;
    esac

    return 0
    
}
complete -F _comppll dns

