/************************************
Course: cse 251
File: team1.java
Week: week 11 - team activity 1

Instructions:

- Main contains an array of 1,000 random values.  You will be creating
  threads to process this array.  If you find a prime number, display
  it to the console.

- DON'T copy/slice the array in main() for each thread.

Part 1:
- Create a class that is a sub-class of Thread.
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 2:
- Create a class on an interface or Runnable
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 3:
- Modify part1 or part 2 to handle any size array and any number
  of threads.

************************************/
import java.util.Random; 
import java.lang.Math; 

class My_Thread extends Thread
{
  int[] array;
  int start;
  int end;

  public My_Thread(int[] array, int start, int end)
  {
    this.array = array;
    this.start = start;
    this.end = end;
  }

  public void run()
  {
    for (int i = start; i < end; i++) 
    {
      if (isPrime(array[i]))
      {
        System.out.println(array[i]);
      }
    }
  }



  static boolean isPrime(int n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (int i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }
}

class My_Interface implements Runnable
{
  int[] array;
  int start;
  int end;

  public My_Interface(int[] array, int start, int end)
  {
    this.array = array;
    this.start = start;
    this.end = end;
  }

  public void run()
  {
    for (int i = start; i < end; i++) 
    {
      if (isPrime(array[i]))
      {
        System.out.println(array[i]);
      }
    }
  }

  static boolean isPrime(int n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (int i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }
}

class Main {

  static boolean isPrime(int n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (int i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }

  public static void main(String[] args) {
    System.out.println("Hello world!");

    // create instance of Random class 
    Random rand = new Random();

    int count = 1000;
    int[] array = new int[count];
    for (int i = 0; i < count; i++) {
      array[i] = Math.abs(rand.nextInt());
    }

    My_Thread [] threads = new My_Thread[4];
    for (int i = 0; i < 4; i++) {
      threads[i] = new My_Thread(array, i * count / 4, (i + 1) * count / 4);
      threads[i].start();
    }

    My_Interface [] interfaces = new My_Interface[4];
    for (int i = 0; i < 4; i++) {
      interfaces[i] = new My_Interface(array, i * count / 4, (i + 1) * count / 4);
      interfaces[i].run();
    }

    // for (int i = 0; i < count; i++) {
    //   if (isPrime(array[i])) {
    //     System.out.println(array[i]);
    //   }
    // }
  }
}