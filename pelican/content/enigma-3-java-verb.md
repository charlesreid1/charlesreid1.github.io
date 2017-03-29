Title: Enigma Cipher Implementation: Part 3: Enigma in Java Without Objects
Date: 2017-03-22 18:00
Category: Enigma
Tags: ciphers, enigma, encryption, java

As the title suggests, we're continuing with the third in a series of posts 
exploring a verb-oriented approach to programming - 
in an attempt to free ourselves from the fetishization of objects,
we are attempting to learn how to use languages against their will.

This is all inspired by [Steve Yegge's 2006 blog post](http://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html),
"Execution in the Kingdom of Nouns," an excellent read that inspired me to 
explore the subject more deeply. 

## Java Pseudocode

In the last post, we ran through the pseudocode for an Enigma machine 
based entirely upon Strings, iterators, and integer indexes, 
leading to a vastly simpler abstraction of the Enigma machine
than would have resulted if we had implicitly chosen a noun-centric approach,
divided the entire Enigma encryption process into its component nouns like rotor wheels and reflectors,
and implemented each as an object.

Here was the pseudocode:

```plain
define plaintext message
define normal alphabet and scrambled alphabets
define list of switchboard swap pairs
define list of reflector swap pairs
for each character in plaintext message:

    # Apply switchboard transformation
    for each pair in switchboard swap pairs:
        if character in swap pair, swap its value

    # Apply forward rotor transformation
    for each scrambled alphabet:
        get index of character in normal alphabet
        get new character at that index in scrambled alphabet
        replace character with new character 

    # Apply reflector transformation
    for each pair in reflector swap pairs:
        if character in swap pair, swap its value

    # Apply reverse rotor transformation
    for each scrambled alphabet:
        get index of input character in scrambled alphabet
        get new character at that index in normal alphabet
        replace character with new character 

    # Apply switchboard transformation
    for each pair in switchboard swap pairs:
        if character in swap pair, swap its value

    concatenate transformed input character to ciphertext message 

    # Increment rotor wheels
    for each rotor/scrambled alphabet, left to right:
        get index of left notch in left alphabet
        get index of right notch in right alphabet
        if left index equals right index:
            cycle left alphabet forward 1 character
    cycle right-most alphabet forward 1 character
```

## Java Code

The Enigma code is defined in the Java program as follows:

* The Enigma class defines a set of constants for historically accurate cipher settings.
* The main method contains the encryption procedure.
* There is one static helper method called rotateString.

Everything is in a public class. Starting with the definitions of constants:

```java
public class Enigma {

    public static final String ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    
    // Historically accurate rotor scrambles
    // See http://www.codesandciphers.org.uk/enigma/rotorspec.htm
    public static final String[] WHEEL = { ALPHA,
                        "EKMFLGDQVZNTOWYHXUSPAIBRCJ", // Rotor I    - Royal
                        "AJDKSIRUXBLHWTMCQGZNPYFVOE", // Rotor II   - Flags
                        "BDFHJLCPRTXVZNYEIWGAKMUSQO", // Rotor III  - Wave
                        "ESOVPZJAYQUIRHXLNFTGKDCMWB", // Rotor IV   - Kings
                        "VZBRGITYUPSDNHLXAWMJQOFECK", // Rotor V    - Above
                        "JPGVOUMFYQBENHZRDKASXLICTW",
                        "NZJHGRCXMYSWBOUFAIVLPEKQDT",
                        "FKQHTLXOCBJSPDZRAMEWNIUYGV"};

    // Knocking (notch and clasp) advances the wheel to the left
    public static final String[] NOTCH = {"",  // No notch
                                          "R", // Royal
                                          "F", // Flags
                                          "W", // Wave
                                          "K", // Kings
                                          "A", // Above
                                          "AN",
                                          "AN",
                                          "AN"};

    // Reflectors
    public static final String REFLECTOR_ALPHA = "AY:BR:CU:DH:EQ:FS:GL:IP:JX:KN:MO:TZ:VW";

```

## Main Method: User Settings

The next part of the code is the main method, where we begin by defining variables 
that correspond to settings that the Enigma operator would set from the daily Enigma code book.
These included:

* The numbering and ordering of wheels (e.g., `IV II I`)
* The initial rotor settings for each wheel (position 0-25)
* The pairs of letters connected on the switch board

The wheels are specified using the `WHEEL` array of Strings, above.
Each element of the WHEEL array contains a different scrambled alphabet, 
corresponding to the alphabet scrambles hard-coded into the historical rotor wheels.
These go into `rotorAlpha`, which stores each rotor's alphabet in a String.

The locations of the notches that advance neighboring wheels are fixed by the choice of wheels, 
and are available through the `NOTCH` array.
The notch locations implemented in `NOTCH` are historically accurate for each rotor wheel. 

The initial rotor settings were also contained in the code book as a sequence of 3 numbers,
each 0-25, indicating how many turns each wheel was rotated before starting.

The plugboard pairs specify the wired connections on the front of the machine.
These plugboard pairs were also daily machine settings specified in the daily Enigma code book.
The plugboard pairs are input as a single string, with pairs of letters separated by a ":", like this: `AB:CD:EF:GH`.
Pairs must be unique (no letter can connect to itself). 
Letters cannot be repeated (no letter can connect to more than 1 other letter).

```java
    public static void main(String[] args) { 

        // These two strings should encrypt/decrypt to each other when you run them through the Enigma.
        //String message = "ABCDE FG HIJKL MNOP QRS TUVWXYZ"; 
        String message = "TVVFT KS UNVYJ FAFV NPC DZJPWEJ";


        //////////////////////////////////
        // Operator Settings
        // 
        // Enigma operators have code sheets that specify: 
        //  - The numbering/ordering of wheels 
        //  - The initial rotor settings
        //  - The plugboard pairs

        // Rotor scrambles are applied right-to-left
        //              {LAST, MIDDLE, FIRST}
        String[] rotorAlpha = {WHEEL[1],WHEEL[2],WHEEL[3]};
        String[] rotorNotch = {NOTCH[1],NOTCH[2],NOTCH[3]};
        int[] rotorInit = {0,0,0};

        String plugboardPairs = "IR:HQ:NT:WZ:VC:OY:GP:LF:BX:AK";

        String coded = enigma(message, rotorAlpha, rotorNotch, rotorInit, plugboardPairs);
        System.out.println(coded);
    }
```

## Cipher Procedure

The next bit of code is the meat of the Enigma method.
Notice that this is purely procedural code, and makes no use of objects other than the built-in String type. 
This is the kind of verb-oriented code we are striving for
when we write noun-free Java code.

We also pass in any information that's required. 
Normally we would wrap all of these quantities in an object,
to keep the list of parameters short, but this implementation is entirely object-free.

```java
    public static String enigma(String message,
                                String[] rotorAlpha,
                                String[] rotorNotch,
                                int[] rotorInit,
                                String[] plugboardPairs) { 

        StringBuilder message_final = new StringBuilder();

        //////////////////////////////////////
        // Enigma Cipher

        // Apply each transformation in sequence
        for(int i=0; i<message.length(); i++) {

            // Starting char
            char c_orig = message.charAt(i);
            char c = c_orig;

            // Perform plugboard swap
            for(String pair : plugboardPairs.split(":")) {
                if(c==pair.charAt(0)) {
                    c = pair.charAt(1);
                } else if(c==pair.charAt(1)) {
                    c = pair.charAt(0);
                }
            }

            // Perform rotor letter substitutions
            // (forward order: right-to-left)
            int ix = -100;
            for(int j=(rotorAlpha.length-1); j>=0; j--) { 
                ix = ALPHA.indexOf(c);
                String thisAlpha = rotorAlpha[j];
                if(ix>=0) { 
                    c = thisAlpha.charAt(ix);
                } else {
                    c = c_orig;
                }
            }

            // Perform reflection
            for(String pair : REFLECTOR_ALPHA.split(":")) {
                if(c==pair.charAt(0)) {
                    c = pair.charAt(1);
                } else if(c==pair.charAt(1)) {
                    c = pair.charAt(0);
                }
            }

            // Perform rotor letter substitutions
            // (backwards order: left-to-right) 
            ix = -100;
            for(int j=0; j<rotorAlpha.length; j++) { 
                String thisAlpha = rotorAlpha[j];
                ix = thisAlpha.indexOf(c);
                if(ix>=0) { 
                    c = ALPHA.charAt(ix);
                } else {
                    c = c_orig;
                }
            }


            // Perform plugboard swap
            for(String pair : plugboardPairs.split(":")) {
                if(c==pair.charAt(0)) {
                    c = pair.charAt(1);
                } else if(c==pair.charAt(1)) {
                    c = pair.charAt(0);
                }
            }


            // Final text
            if( c>='A' && c<='Z') { 
                message_final.append(c);
            } else {
                // Could not resolve 
                message_final.append(c_orig);
            }

            // Increment rotors
            for(int j=0; j<(rotorAlpha.length-1); j++) {
                String alphaL = rotorAlpha[j];
                int ixL = alphaL.indexOf(rotorNotch[j]);
                String alphaR = rotorAlpha[j+1];
                int ixR = alphaR.indexOf(rotorNotch[j+1]);
                if(ixL!=ixR) { 
                    rotorAlpha[j] = rotateString(rotorAlpha[j]);
                }
            }
            // Always increment the right-most rotor
            int lenny = rotorAlpha.length;
            rotorAlpha[lenny-1] = rotateString(rotorAlpha[lenny-1]);
        }

        return message_final.toString();
    }
```


## Utility Method: String Rotator

One last piece that's needed to emulate the rotation of the rotor wheels 
is a method to rotate strings forward 1 character. Here's that method:

```java
    /// Rotate a string forward by 1 character, so "ABCDEF" becomes "FABCDE"
    public static String rotateString(String original) {
        int lenny = original.length();
        StringBuilder rotated = new StringBuilder();
        rotated.append(original.charAt(lenny-1));
        for(int i=0;i<lenny-1;i++) { 
            rotated.append(original.charAt(i));
        }
        return rotated.toString();
    }

} // end Enigma class
```


## Complete Enigma Implementation

Here is a link to the complete Enigma code on git.charlesreid1.com: [Enigma.java](https://charlesreid1.com:3000/charlesreid1/java-crypto/src/master/enigma/Enigma.java)

Now that the Enigma machine implementation is finished, we can test it out.
One feature of the Enigma that makes it easy to test is, it is symmetric.
If we feed a plain text into the Enigma and get the corresponding ciphertext,
we can feed that ciphertext through the Enigma (with the same initial settings) 
and recover the original plain text.

Running the alphabet through the Enigma yields:

```bash
$ java Enigma
IN:  ABCDE FG HIJKL MNOP QRS TUVWXYZ
OUT: TVVFT KS UNVYJ FAFV NPC DZJPWEJ
```

Running this back through the Enigma yields:

```bash
$ java Enigma
IN:  TVVFT KS UNVYJ FAFV NPC DZJPWEJ
OUT: ABCDE FG HIJKL MNOP QRS TUVWXYZ
```

**NOTE:** This code modifies the Enigma machine's settings in-place.
This means multiple sequential calls to the `enigma()` method will not reset the rotors.
The following code will not recover the original plain text `message`:

```java
// This won't work:
String coded = enigma(message, rotorAlpha, rotorNotch, rotorInit, plugboardPairs);
String original2 = enigma(coded, rotorAlpha, rotorNotch, rotorInit, plugboardPairs);
```

To do this correctly, we would need multiple copies of the input arrays `rotorAlpha`, `rotorNotch`, and `rotorInit`:

```java
String plugboardPairs = "IR:HQ:NT:WZ:VC:OY:GP:LF:BX:AK";

String[] rotorAlpha = {WHEEL[1],WHEEL[2],WHEEL[3]};
String[] rotorNotch = {NOTCH[1],NOTCH[2],NOTCH[3]};
int[] rotorInit = {0,0,0};
String coded = enigma(message, rotorAlpha, rotorNotch, rotorInit, plugboardPairs);

String[] rotorAlpha2 = {WHEEL[1],WHEEL[2],WHEEL[3]};
String[] rotorNotch2 = {NOTCH[1],NOTCH[2],NOTCH[3]};
int[] rotorInit2 = {0,0,0};
String original = enigma(coded, rotorAlpha2, rotorNotch2, rotorInit2, plugboardPairs);

System.out.println("ORIGINAL:  "+message);
System.out.println("RECOVERED: "+original);
```

This works fine:

```
ORIGINAL:  ABCDE FG HIJKL MNOP QRS TUVWXYZ
RECOVERED: ABCDE FG HIJKL MNOP QRS TUVWXYZ 
```


## Sources

1. "Execution in the Kingdom of Nouns". Steve Yegge. March 2006. Accessed 18 March 2017.
<[https://web.archive.org/web/20170320081755/https://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html](https://web.archive.org/web/20170320081755/https://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html)>

2. "The Enigma Cipher". Tony Sale and Andrew Hodges. Publication date unknown. Accessed 18 March 2017.
<[https://web.archive.org/web/20170320081639/http://www.codesandciphers.org.uk/enigma/index.htm](https://web.archive.org/web/20170320081639/http://www.codesandciphers.org.uk/enigma/index.htm)>

