### **MISSION CONTEXT**

We know that stars generally fall into three categories:

1. Blue Stars: Very hot, young, and bright.  
2. Red Stars: Cooler, often older (Red Giants).  
3. Faint White Stars: Dead remnants (White Dwarfs).

### **YOUR DATA**

You have a dataset containing the magnitude (brightness) of stars in five different color filters:

* Ultraviolet (u)  
* Green (g)  
* Red (r)  
* Infrared (i)  
* Zeta (z)

### **THE CHALLENGE**

Computers cannot "learn" yet. You must manually program the rules to classify these stars.

Data: [Skyserver\_CrossID1\_13\_2026 4\_47\_50 PM.xlsx](https://docs.google.com/spreadsheets/d/1UrCTBo9qUChArXnKEyCNP6E1u8OkrAN-/edit?usp=sharing&ouid=100735936960872459269&rtpof=true&sd=true)

### **TASK REQUIREMENTS**

1. Load the Data: Import the dataset into a Pandas DataFrame.  
2. Create "Color" Features:  
   * Create a new column 'u\_g' by subtracting the Green magnitude from the Ultraviolet magnitude (u-g). 

   This roughly represents the **temperature**.

3. The Manual Classifier  
   * Write a function classify\_star(row) that uses hard-coded thresholds (if/else statements) to assign a label: "Blue", "Red", or "Dwarf".

   Example logic:  
     `if row['u_g'] < 0.5:`  
     `return 'Blue'`

     
     NOTE: You have to guess the numbers\! Look at the data and try to find a cutoff point where one type of star ends and another begins.

4. Visualize  
   Create a scatter plot:  
   * X-axis: u \- g (Color)  
   * Y-axis: r (Brightness)

Color the points based on your manual labels.

### **DELIVERABLE**

Submit your code and the resulting plot.

* Be prepared to discuss the following question in the next session: "How confident are you in the specific numbers you chose for your cutoffs?"  
* What else method can YOU think of?

