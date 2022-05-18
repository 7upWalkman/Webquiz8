////////////////////////////////////////////////////////////////////////////////
///
///      POO EM JAVASCRIPT
///
///      Breves exemplos utilizando os seguinte modelos:
///
///      1. Sem Classes: Fábricas de Objectos c/ "Herança" Funcional
///      2. Clássico: Classes ES6
///
////////////////////////////////////////////////////////////////////////////////


/*
 *  OBJECTOS LITERAIS, MÉTODOS E THIS
 *
 *  Preliminar alguns aspectos relacionados com objectos literais
 *  Definições de Métodos e o objecto THIS
 */

let obj1 = {
    x: 23,
    fun1: function() {
        return this.x;
    },
    fun2() {
        return this.x;
    },
    fun3: () => this.x,     // provavelmente dá erro...
    fun4: () => {
        return this.x;      // provavelmente dá erro...
    },
}

obj1.fun1();   // 23
obj1.fun2();   // 23
obj1.fun3();   // undefined
obj1.fun4();   // undefined

/*
 *  NEW E THIS
 *  
 *  Podemos utilizar o NEW para criar objectos. Mas será que 
 *  funciona como em Java ou C#? Quais as desvantagens?
 * 
 *  Aqui só nos focamos em NEW. No entanto, para perceber melhor
 *  o NEW, aconselha-se o estudo do modelo de objectos do JS,
 *  em particular o que são protótipos, o que permitem, e como 
 *  se consegue herança com estes protótipos.
 */

function Obj() {
    this.x = 23;
    this.fun1 = function() {
            return this.x;
    };
    this.fun3 = () => this.x;       // não dá erro se Obj chamado com new
    this.fun4 = () => {
        return this.x;              // não dá erro se Obj chamado com new
    };
    // não é preciso return porque o NEW garante que o THIS é devolvido
}

obj1 = new Obj();
obj1.fun1();   // 23
obj1.fun3();   // 23
obj1.fun4();   // 23

// Problema: e se não usarmos o new quando invocamos Obj?
//      obj1 = Obj();       // BRONCA!

/*
 *  FÁBRICA DE OBJECTOS: FUNÇÕES, CLOSURES E OBJECTOS LITERAIS EM VEZ 
 *  DE NEW E THIS.
 *
 *  As funções de JavaScript são extramente poderosas e flexíveis.
 *  Juntamente com a "maquinaria" para closures, não precisamos de
 *  manipular protótipos directamente, nem de classes ES6 (que são
 *  classes ao estilo de Java e não encaixam tão bem numa linguagem
 *  funcional como é o caso de JavaScript).
 */

function make_obj() {
    let x = 23;
    return {
        fun1: function() {
            return x;
        },
        fun2() {
            return x;
        },
        fun3: () => x,   // ok
        fun4: () => {
            return x;
        }
    };
}

obj1 = make_obj();
obj1.fun1();   // 23
obj1.fun2();   // 23
obj1.fun3();   // 23
obj1.fun4();   // 23

/*
 *  FÁBRICA DE OBJECTOS: OUTRA ALTERNATIVA
 */

function make_obj() {
    let x = 23;
    let that = {};
    
    that.fun1 = function() {
        return x;
    };
    that.fun3 = () => x;
    that.fun4 = () => {
        return x;
    };

    // Se o objecto estiver completo podemos logo devolver o objecto
    //
    //      return that;
    // 
    // Se quisermos ainda acrescentar propriedades, podemos fazer:
    return {
        ...that, 
        fun2() { 
            return x;
        }
    };
}

obj1 = make_obj();
obj1.fun1();   // 23
obj1.fun2();   // 23
obj1.fun3();   // 23
obj1.fun4();   // 23

////////////////////////////////////////////////////////////////////////////////
///
///      POO SEM CLASSES: FÁBRICAS DE OBJECTOS C/ "HERANÇA" FUNCIONAL
///      Ideia geral: utilizar o scope das funções para conservar 
///      valores e objectos privados, closures para reter esses objectos,
///      e objectos literais para devolver uma unidade agregada de 
///      propriedades (atributos e métodos) relacionadas. 
///
///      Dito de outra forma, os métodos de cada objecto devolvido são
///      closures que capturam as variáveis locais (e privadas) da
///      função construtora.
///
///      Mecanismos como Object.freeze permitem a devolução de objectos
///      imutáveis.
///
////////////////////////////////////////////////////////////////////////////////

// 1a ALTERNATIVA

function pessoa(nomeCompleto, dataNasc, emailAddr) {
    // Podemos inserir aqui validações; eg: email inválido, data 
    // inválida, etc.
    return {
        primNome: () => nomeCompleto.split(' ')[0],
        ultmNome: () => nomeCompleto.split(' ').slice(-1)[0],
        idade() {
            let today = new Date();
            let [month, day] = [today.getMonth() + 1, today.getDate()];
            let idade = today.getFullYear() - dataNasc.year;
            if (dataNasc.month > month || 
                dataNasc.month === month && dataNasc.day > day) {
                idade -= 1;
            }
            return idade;
        },
        emailAddr() {
            return emailAddr;
        },
        setEmailAddr(newEmailAddr) {
            emailAddr = newEmailAddr;
        },
    };
}

p1 = pessoa('Alberto Antunes', {year: 2002, month: 11, day: 25}, 'alb@mail.com');
p2 = pessoa('Armando Alves', {year: 1999, month: 6, day: 1}, 'alb@mail.com');

p1.primNome();
p1.ultmNome();
p1.nomeCompleto; // não funciona => é privado...    
p1.dataNasc;     // não funciona => é privado...
p1.idade();
p1.setEmailAddr('alberto@mail.com');
p1.emailAddr();

// 2a ALTERNATIVA: Melhoria da 1a:
//      1) Parâmetros vão num objecto (obj. de especificação) para não de
//         depender da ordem e para tornar código mais legível pq somos 
//         obrigados a usar nomes
//      2) Usamos get e set do ES6
//      3) Opcional: vamos identificar os nosso objecto com uma etiqueta
//         que indica o que são. Uma espécie de tipo de dados.

function pessoa({nomeCompleto, dataNasc, emailAddr}) {
    // Podemos inserir aqui validações; eg: email inválido, data 
    // inválida, etc.
    return {
        get primNome() { 
            return nomeCompleto.split(' ')[0]; 
        },
        get ultmNome() { 
            return nomeCompleto.split(' ').slice(-1)[0];
        },
        get idade() {
            let today = new Date();
            let [month, day] = [today.getMonth() + 1, today.getDate()];
            let idade = today.getFullYear() - dataNasc.year;
            if (dataNasc.month > month || 
                dataNasc.month === month && dataNasc.day > day) {
                idade -= 1;
            }
            return idade;
        },
        get emailAddr() {
            return emailAddr;
        },
        set emailAddr(newEmailAddr) {
            emailAddr = newEmailAddr;
        },
        [Symbol.toStringTag]: 'Pessoa',
    };
}

p1 = pessoa({
    nomeCompleto: 'Alberto Antunes', 
    dataNasc: {year: 2002, month: 11, day: 25}, 
    emailAddr: 'alb@mail.com',
});
p2 = pessoa({
    emailAddr: 'alb@mail.com',
    nomeCompleto: 'Armando Alves', 
    dataNasc: {year: 1999, month: 6, day: 1}, 
});

p1.primNome;
p1.ultmNome;
p1.nomeCompleto; // continua a não funcionar => é privado...
p1.dataNasc;     // continua a não funcionar => é privado...
p1.idade;
p1.emailAddr = 'alberto@mail.com';
p1.emailAddr;
p1.toString();

////////////////////////////////////////////////////////////////////////////////
///
///     POO COM CLASSES ES6
///     O ES6/2015 introduziu um mecanismo de classes inspirado na 
///     linguagem Java. No entanto, para manter compatibilidade com o
///     "sistema" de objectos do JS, este mecanismo de classes é, na 
///     prática, açúcar sintático para facilitar a utilização do 
///     mecanismo original de protótipos e herança prototipal.
///
////////////////////////////////////////////////////////////////////////////////

class Pessoa {
    constructor({nomeCompleto, dataNasc, emailAddr}) {
        this._nomeCompleto = nomeCompleto;    // ES2022: #nomeCompleto
        this._dataNasc = dataNasc;
        this._emailAddr = emailAddr;
    }

    get primNome() { 
        return this._nomeCompleto.split(' ')[0]; 
    }

    get ultmNome() { 
        return this._nomeCompleto.split(' ').slice(-1)[0];
    }

    get idade() {
        let today = new Date();
        let [month, day] = [today.getMonth() + 1, today.getDate()];
        let idade = today.getFullYear() - this._dataNasc.year;
        if (this._dataNasc.month > month || 
            this._dataNasc.month === month && this._dataNasc.day > day) {
            idade -= 1;
        }
        return idade;
    }

    get emailAddr() {
        return this._emailAddr;
    }

    set emailAddr(newEmailAddr) {
        this._emailAddr = newEmailAddr;
    }
}

p1 = new Pessoa({
    nomeCompleto: 'Alberto Antunes', 
    dataNasc: {year: 2002, month: 11, day: 25}, 
    emailAddr: 'alb@mail.com',
});
p2 = new Pessoa({
    emailAddr: 'alb@mail.com',
    nomeCompleto: 'Armando Alves', 
    dataNasc: {year: 1999, month: 6, day: 1}, 
});

p1.primNome;
p1.ultmNome;
p1.nomeCompleto; // continua a não funcionar => é privado...
p1.dataNasc;     // continua a não funcionar => é privado...
p1.idade;
p1.emailAddr = 'alberto@mail.com';
p1.emailAddr;
p1.toString();

