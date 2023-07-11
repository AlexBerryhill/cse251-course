/* ---------------------------------------
Course: CSE 251
Lesson Week: ?12
File: team.go
Author: Brother Comeau

Purpose: team activity - finding primes

Instructions:

- Process the array of numbers, find the prime numbers using goroutines

worker()

This goroutine will take in a list/array/channel of numbers.  It will place
prime numbers on another channel

readValue()

This goroutine will display the contents of the channel containing
the prime numbers

--------------------------------------- */
package main

import (
	"fmt"
	"math/rand"
	"time"
)

func isPrime(n int) bool {
	// Primality test using 6k+-1 optimization.
	// From: https://en.wikipedia.org/wiki/Primality_test

	if n <= 3 {
		return n > 1
	}

	if n%2 == 0 || n%3 == 0 {
		return false
	}

	i := 5
	for (i * i) <= n {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
		i += 6
	}
	return true
}

func worker(start int, end int, channel chan int) {
	for i := start; i < end; i++ {
		if isPrime(i) {
			channel <- i
		}
	}
}

func readValues(channel chan int) {
	for {
		fmt.Println(<-channel)
	}
}

func main() {

	workers := 10
	numberValues := 100

	// Create any channels that you need
	ch := make(chan int)
	// Create any other "things" that you need to get the workers to finish(join)
	// var wg sync.WaitGroup

	// create workers
	for w := 1; w <= workers; w++ {
		go worker(w, w, ch) // Add any arguments
	}

	rand.Seed(time.Now().UnixNano())
	for i := 0; i < numberValues; i++ {
		// ch <- rand.Int()
	}

	// Wait for the workers to finish
	// wg.Wait()

	go readValues(ch) // Add any arguments

	fmt.Println("All Done!")
}
