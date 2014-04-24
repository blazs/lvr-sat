// 
// We copied the code from http://cgi.csc.liv.ac.uk/~konev/SAT14/ 
// Authors are Boris Konev and Alexei Lisista
// 

#include <iostream>
#include <assert.h>
#include <math.h>
#include <vector>
#include <cstdlib>

#define LENGTH length
#define DISCREPANCY discrepancy
#define BITS bits
//#define KBOUND 358

#define MAX_BIT (BITS-1)

int length = 0;
int discrepancy = 0;
int bits = 0;

//auto  bs = new unsigned int[N+1][N+1][BITS];
std::vector< std::vector< std::vector<unsigned int> > > bs;
std::vector< unsigned int >  ps;
int totalNum = 0;
int totalClauses = 0;
int BRK = 0;


void init() {
    ps.resize(LENGTH+2);

    bs.resize(LENGTH+2);
    for (int i = 0; i < LENGTH/2 + 1; i++) {
        bs[i].resize(LENGTH+2);
            for (int j = 0; j < LENGTH+2; j++) {
                bs[i][j].resize(BITS);
            }
    }
    // initialising the arrays to use numbers in place of propositions
    // first, propositions for sequence members
    // p[i] being true means that the i-th member of the sequence is 1
    // p[i] being false means that the i-th member of the sequence is -1
    std::cout << "c This table represents how propositions correspond to numbers" << std::endl;
    std::cout << "c    ";
    for (int ii =1; ii<=LENGTH; ii++)
    {
        ps[ii] = ++totalNum;
        std::cout << "p["  << ii << "] = " << ps[ii] << ", ";
    }
    std::cout << std::endl << std::endl;


    BRK = ++totalNum;
    std::cout << "c    break = " << BRK << std::endl << std::endl;

    // now introduce number for bit vectors encoding the states of an
    // automaton
    //for (int kk = 1; 2*kk < (LENGTH+1); kk++) {
    //for (int kk = 1; kk <= KBOUND ; kk++) {
    for (int kk = 1; (DISCREPANCY+1)*kk <= LENGTH; kk++) {
        for (int iii = 1; iii <= (LENGTH)/kk+1; iii++)
        {
            std::cout << "c    ";
            for (int bit = MAX_BIT ; bit >=0; bit --)
            {
                bs[kk][iii][bit]=++totalNum;
                std::cout << "b[" << kk << "][" << iii << "][" << bit << "] = " << bs[kk][iii][bit] << " ";
            }
            std::cout << std::endl;
        }
        std::cout << std::endl;
    }

    // finally, counting the number of clauses to be printed
    totalClauses = 1; // automaton does not break
    //for (int kk = 1; 2*kk < (LENGTH+1); kk++) {
    //for (int kk = 1; kk<=KBOUND; kk++) {
    for (int kk = 1; (DISCREPANCY+1)*kk <= LENGTH; kk++) {
    
        totalClauses += BITS; // BITS start clauses 
        for (int iii = 1; iii <= (LENGTH)/kk; iii++)
        {
                // for every value -DISCREPANCY..DISCREPANCY we have 
                // BITS rules for +1 and BITS rules for -1 
                totalClauses += 2*BITS*(2*DISCREPANCY); 
                totalClauses += 2; // BAD -> break
                totalClauses += 2*((1<<MAX_BIT)-DISCREPANCY)-1; // Disallowed clauses
        }
    }
    // print the DIMACS header
        std::cout << "p cnf " << totalNum << " " << totalClauses << std::endl<<std::endl<<std::endl;
        std::cout << "c Automaton should not be broken " << std::endl;
        std::cout << "c    -break " << std::endl;
        std::cout << -BRK << " 0" << std::endl << std::endl;
}

// return the symbol representing the sign of the input
char getSignChar(int sign) {
    return (sign > 0)?' ':'-';
}

// return the symbol representing the negated sign of the input
char getNegSignChar(int sign) {
    return (sign > 0)?'-':' ';
}

// return 1 if the i-th bit in the binary representation of state is 1 and 
// -1 if it is 0
int getBitSign(int state, int bit) {
    if ((bit == MAX_BIT)) {
        return (state < 0)?1:-1;
    }

    assert(bit < MAX_BIT);

    if(state < 0) state *=-1;

    return ((state & (1<<bit))?1:-1);
}

// get the sign of the bit representing state
char getBitSignChar(int state, int bit) {
    return getSignChar(getBitSign(state, bit));
}

// get the negated sign of the bit representing state (used in rules of the
// form (state & p) -> state'
char getNegBitSignChar(int state, int bit) {
    return getNegSignChar(getBitSign(state, bit));
}

// print the negated bit vector representing state. k and i a parameters to
// define the jumps over the input sequence
void printState(int state, int k, int i) {
    for (int j = MAX_BIT; j >= 0; j--) {
        std::cout << "" << getBitSignChar(state, j) << "b^{" << k << ", " << i << "}_" << j << " ? ";
    }
}

// print the negated bit vector representing state. k and i a parameters to
// define the jumps over the input sequence
void printStateNeg(int state, int k, int i) {
    for (int j = MAX_BIT; j >= 0; j--) {
        std::cout << "" << getNegBitSignChar(state, j) << "b^{" << k << ", " << i << "}_" << j << " ? ";
    }
}

// print the negated bit vector representing state in the DIMACS format. 
// k and i a parameters to define the jumps over the input sequence
void printStateNegDIMACS(int state, int k, int i) {
    for (int j = MAX_BIT; j >=0;  j--) {
        std::cout << "" << getNegBitSignChar(state, j) << bs[k][i][j] << " ";
    }
}


// print an automaton transition rule form state 1 to state 2 reading an input
// at position k*i. 
void printRule(int state1, int seqSign, int state2, int k, int i) {


    std::cout << "c    (";
    printState(state1, k, i);
    std::cout << "" << getSignChar(seqSign) << "p_" << k*i << ") -> (";
    for (int j = MAX_BIT; j > 0 ; j--) {
        std::cout << getBitSignChar(state2,j) << "b^{" << k << ", " << (i+1) << "}_" << j << " ? ";
    }
    std::cout << getBitSignChar(state2,0) << "b^{" << k << ", " << (i+1) << "}_" << 0 << ")" << std::endl;

    std::cout << "c  in CNF:" << std::endl;
    for (int j = MAX_BIT; j >= 0 ; j--) {
        std::cout << "c    ";
        printStateNeg(state1, k, i);
        std::cout << "" << getNegSignChar(seqSign) << "p_" << k*i << " ? ";
        std::cout << getBitSignChar(state2,j) << "b^{" << k << ", " << (i+1) << "}_" << j << std::endl;
    }
}

// print an automaton transition rule form state 1 to state 2 reading an input
// at position k*i in the DIMACS format 
void printRuleDIMACS(int state1, int seqSign, int state2, int k, int i) {
    std::cout << "c  in DIMACS:" << std::endl;
    for (int j = MAX_BIT; j >= 0; j--) {
        printStateNegDIMACS(state1, k, i);
        std::cout << "" << getNegSignChar(seqSign) << ps[k*i] << " ";
        std::cout << getBitSignChar(state2,j) << bs[k][(i+1)][j];
        std:: cout << " 0" << std::endl;
    }
}



// print an automaton transition rule form state 1 to state 2 reading an input
// at position k*i. 
void printBRKRule(int state1, int seqSign, int k, int i) {
    std::cout << "c    (";
    printState(state1, k, i);
    std::cout << "" << getSignChar(seqSign) << "p_" << k*i << ") -> break" << std::endl;
    std::cout << "c  in CNF:" << std::endl;

    std::cout << "c    ";
    printStateNeg(state1, k, i);
    std::cout << "" << getNegSignChar(seqSign) << "p_" << k*i << " ? ";
    std::cout << "break" << std::endl;
}

// print an automaton transition rule form state 1 to state 2 reading an input
// at position k*i in the DIMACS format 
void printBRKRuleDIMACS(int state1, int seqSign, int k, int i) {
    std::cout << "c  in DIMACS:" << std::endl;
    printStateNegDIMACS(state1, k, i);
    std::cout << "" << getNegSignChar(seqSign) << ps[k*i] << " ";
    std::cout << BRK;
    std:: cout << " 0" << std::endl;
}




// always start in state 0 and i=1
void printStartStateCNF(int k) {
    for (int bit = MAX_BIT; bit >= 0; bit --) {
        std::cout << "c    " << "-b^{" << k << ", " << 1 << "}_" << bit << std::endl;
    }
}

// always start in state 0 and i=1. In the DIMACS format
void printStartStateDIMACS(int k) {
    std::cout << "c  in DIMACS:" << std::endl;
    for (int bit = MAX_BIT; bit >= 0; bit --) {
        std::cout << "-" << bs[k][1][bit] << " 0" << std::endl;
    }
}


// print the start state of the automaton
void printStartState(int k) {
    printStartStateCNF(k);
    printStartStateDIMACS(k);
    std::cout << std::endl;
}


void printDisallowedCombinations(int k, int i) {
    std::cout << "c Disallowed combinations" << std::endl;
    std::cout << "c  0b100 represents a \"negated\" zero. Not a state." << std::endl; 
    std::cout << "c    -(";
    printState(-(1<<MAX_BIT), k, i);
    std::cout << "true) " << std::endl;

    std::cout << "c  in CNF:" << std::endl;
    std::cout << "c    ";
    printStateNeg(-(1<<MAX_BIT), k, i);
    std::cout << "false " << std::endl;

    std::cout << "c  in DIMACS:" << std::endl;
    printStateNegDIMACS(-(1<<MAX_BIT), k, i);
    std::cout << " 0" << std::endl;
    std::cout << std::endl;

    for (int num = DISCREPANCY+1; num < (1<<MAX_BIT); num++)
    {
        std::cout << "c  " << num << " does not represent an automaton state." << std::endl;
        std::cout << "c    -(";
        printState(num, k, i);
        std::cout << "true) " << std::endl; // just to make the line syntactically correct
        std::cout << "c  in CNF:" << std::endl;

        std::cout << "c    ";
        printStateNeg(num, k, i);
        std::cout << "false " << std::endl; // just to make the line syntactically correct

        std::cout << "c  in DIMACS:" << std::endl;
        printStateNegDIMACS(num, k, i);
        std::cout << " 0" << std::endl;

        std::cout << "c  " << -num << " does not represent an automaton state." << std::endl;
        std::cout << "c    -(";
        printState(-num, k, i);
        std::cout << "true) " << std::endl; // just to make the line syntactically correct
        std::cout << "c  in CNF:" << std::endl;

        std::cout << "c    ";
        printStateNeg(-num, k, i);
        std::cout << "false " << std::endl; // just to make the line syntactically correct

        std::cout << "c  in DIMACS:" << std::endl;
        printStateNegDIMACS(-num, k, i);
        std::cout << " 0" << std::endl;

        std::cout << std::endl;
        /* for some reasons unknown, the following performs 10-15% worse
         * than having 2 different clauses disallowing separately num and 
         * -num  as above
        std::cout << "c  Neither " << num << " nor " << -num << " represent an automaton state." << std::endl;
        std::cout << "c  Can be represented by just one clause with the sign bit omitted." << std::endl; 
        std::cout << "c    -(";
        //printState(num, k, i);

        for (int j = MAX_BIT-1; j >= 0; j--) {
            std::cout << "" << getBitSignChar(num, j) << "b^{" << k << ", " << i << "}_" << j << " ? ";
        }
        std::cout << "true) " << std::endl;
        std::cout << "c  in CNF:" << std::endl;

        std::cout << "c    ";
        //printStateNeg(num, k, i);
        for (int j = MAX_BIT-1; j >= 0; j--) {
            std::cout << "" << getNegBitSignChar(num, j) << "b^{" << k << ", " << i << "}_" << j << " ? ";
        }
        std::cout << "false " << std::endl;

        std::cout << "c  in DIMACS:" << std::endl;
        for (int j = MAX_BIT-1; j >=0;  j--) {
            std::cout << "" << getNegBitSignChar(num, j) << bs[k][i][j] << " ";
        }
        std::cout << " 0" << std::endl;
        std::cout << std::endl;
        */
    }
}


// print the transition rule for the k-th automaton in the i-th position.
void printRules(int k, int i) {
    for (int d=-DISCREPANCY; d < DISCREPANCY; d++) {
        std::cout << "c  " << d << "+1 --> " << d+1 << std::endl;
        printRule(d, +1, d+1, k, i);
        printRuleDIMACS(d, +1, d+1, k, i);
        std::cout << std::endl;
    }
    std::cout << "c  " << DISCREPANCY << "+1 --> break "  << std::endl;
    printBRKRule(DISCREPANCY, +1, k, i);
    printBRKRuleDIMACS(DISCREPANCY, +1, k, i);
    std::cout << std::endl;
    std::cout << std::endl;


    for (int d=DISCREPANCY; d > -DISCREPANCY; d--) {
        std::cout << "c  " << d << "-1 --> " << d-1 << std::endl;
        printRule(d, -1, d-1, k, i);
        printRuleDIMACS(d, -1, d-1, k, i);
        std::cout << std::endl;
    }
    std::cout << "c  " << -DISCREPANCY << "-1 --> break " << std::endl;
    printBRKRule(-DISCREPANCY, -1,  k, i);
    printBRKRuleDIMACS(-DISCREPANCY, -1, k, i);
    std::cout << std::endl;
    std::cout << std::endl;
}


int main(int argc, char** argv) {
	if (argc > 3) {
		length = atoi(argv[1]);
		discrepancy = atoi(argv[2]);
		bits = atoi(argv[3]);
	} else {
		std::cout << "usage: " << argv[0] << " [length] [discrepancy] [bits]" << std::endl;
		return 1;
	}
	
    assert(2*DISCREPANCY+2 <= (int) pow(2,BITS));

    init();

    //for (int k = 1; 2*k < (LENGTH+1); k++) {
    //for (int k = 1; k<=KBOUND; k++) {
    for (int k = 1; (DISCREPANCY+1)*k <= LENGTH; k++) {
        std::cout << "c INIT for k = " << k << std::endl;
        printStartState(k);
        int i = 1;
        std::cout << "c Transitions for k = " << k << std::endl;
        for( ; i<=(LENGTH)/k; i++) {
            std::cout << "c i = " << i << std::endl;
            printRules(k, i);
            printDisallowedCombinations(k,i);
        }
    }
}
