DIGITOS[0-9]
LETRAS[a-zA-Z]
space[\t\r\n\f]|" "
comentMultiplo[/][*][^*]*[*]+([^*/][^*]*[*]+)*[/]
%{

/*
ALUNOS:
ALEX SANTOS TAVARES,
PEDRO LUIZ QUANZ DE SANT'ANA BARROS,
VITOR HUGO DUARTE DA SILVA,
Felipe Cecconello Fontana
*/

%}

%%

{DIGITOS}+ {fprintf(yyout, "['numeral', '%s']\n", yytext);}

{DIGITOS}+{LETRAS}+({LETRAS}|{DIGITOS})* {fprintf(yyout, "['ERRO LEXICO', '%s']\n", yytext);}

{DIGITOS}+\.{DIGITOS}+ {fprintf(yyout, "['ERRO LEXICO', '%s']\n", yytext);}

"boolean"|"class"|"extends"|"public"|"static"|"void"|"main"|"String"|"return"|"int"|"if"|"else"|"while"|"System.out.println"|"length"|"true"|"false"|"this"|"new"|"null" {fprintf(yyout, "['Palavra reservada', '%s']\n", yytext);}

{LETRAS}+({LETRAS}|{DIGITOS}|"_")* {fprintf(yyout, "['Identificador', '%s']\n", yytext);}

"="|"<"|"=="|"!="|"+"|"-"|"*"|"&&"|"!" {fprintf(yyout, "['Operador', '%s']\n", yytext);}

"("|")"|"["|"]"|"{"|"}"|";"|"."|"," {fprintf(yyout, "['Pontuacao', '%s']\n", yytext);}

{space}+ {}

"//".* {}

{comentMultiplo} {}

. {fprintf(yyout, "['ERRO LEXICO', '%s']\n", yytext);} 

%%

int yywrap(){}
int main(){

FILE *fp, *fw;
char filename[50];
printf("Digite o nome do arquivo: \n");
scanf("%s", filename);
fp = fopen(filename, "r");
yyin = fp;
fw = fopen("saida.txt", "w+");
yyout = fw;

yylex();

fclose(fp);
fclose(fw);

}
