import urllib.request
import unittest
from typing import TypeVar, Callable, List

T = TypeVar('T')
S = TypeVar('S')


#################################################################################
# EXERCISE 1
#################################################################################
def mysort(lst: List[T], compare: Callable[[T, T], int]) -> List[T]:
    if len(lst) == 0: return lst
    l = [lst[0]]  # l is the sorted list
    for i in lst[1:]:
        if compare(i, l[0]) < 1:
            l.insert(0, i)
        elif compare(i, l[-1]) > -1:
            l.append(i)
        else:
            c = 0
            while compare(l[c], i) == -1:
                c += 1
            l.insert(c, i)
    return l


def mybinsearch(lst: List[T], elem: S, compare: Callable[[T, S], int]) -> int:
    iMin = 0
    iMax = len(lst) - 1
    while True:
        a = round((iMin + iMax) / 2)
        if compare(lst[a], elem) == -1:
            iMin = a + 1
        elif compare(lst[a], elem) == 0:
            while compare(lst[a], elem) == 0:
                a -= 1
            return a + 1
        else:
            iMax = a - 1
        if iMin > iMax:
            return -1


class Student():
    """Custom class to test generic sorting and searching."""

    def __init__(self, name: str, gpa: float):
        self.name = name
        self.gpa = gpa

    def __eq__(self, other):
        return self.name == other.name


# 30 Points (total)
def test1():
    """Tests for generic sorting and binary search."""
    print(80 * "#" + "\nTests for generic sorting and binary search.")
    test1_1()
    test1_2()
    test1_3()
    test1_4()
    test1_5()


# 6 Points
def test1_1():
    """Sort ints."""
    print("\t-sort ints")
    tc = unittest.TestCase()
    ints = [4, 3, 7, 10, 9, 2]
    intcmp = lambda x, y: 0 if x == y else (-1 if x < y else 1)
    sortedints = mysort(ints, intcmp)
    tc.assertEqual(sortedints, [2, 3, 4, 7, 9, 10])


# 6 Points
def test1_2():
    """Sort strings based on their last character."""
    print("\t-sort strings on their last character")
    tc = unittest.TestCase()
    strs = ['abcd', 'aacz', 'zasa']
    suffixcmp = lambda x, y: 0 if x[-1] == y[-1] else (-1 if x[-1] < y[-1] else 1)
    sortedstrs = mysort(strs, suffixcmp)
    tc.assertEqual(sortedstrs, ['zasa', 'abcd', 'aacz'])


# 6 Points
def test1_3():
    """Sort students based on their GPA."""
    print("\t-sort students on their GPA.")
    tc = unittest.TestCase()
    students = [Student('Josh', 3.0), Student('Angela', 2.5), Student('Vinesh', 3.8), Student('Jia', 3.5)]
    sortedstudents = mysort(students, lambda x, y: 0 if x.gpa == y.gpa else (-1 if x.gpa < y.gpa else 1))
    expected = [Student('Angela', 2.5), Student('Josh', 3.0), Student('Jia', 3.5), Student('Vinesh', 3.8)]
    tc.assertEqual(sortedstudents, expected)


# 6 Points
def test1_4():
    """Binary search for ints."""
    print("\t-binsearch ints")
    tc = unittest.TestCase()
    ints = [4, 3, 7, 10, 9, 2]
    intcmp = lambda x, y: 0 if x == y else (-1 if x < y else 1)
    sortedints = mysort(ints, intcmp)
    tc.assertEqual(mybinsearch(sortedints, 3, intcmp), 1)
    tc.assertEqual(mybinsearch(sortedints, 10, intcmp), 5)
    tc.assertEqual(mybinsearch(sortedints, 11, intcmp), -1)


# 6 Points
def test1_5():
    """Binary search for students by gpa."""
    print("\t-binsearch students")
    tc = unittest.TestCase()
    students = [Student('Josh', 3.0), Student('Angela', 2.5), Student('Vinesh', 3.8), Student('Jia', 3.5)]
    stcmp = lambda x, y: 0 if x.gpa == y.gpa else (-1 if x.gpa < y.gpa else 1)
    stbincmp = lambda x, y: 0 if x.gpa == y else (-1 if x.gpa < y else 1)
    sortedstudents = mysort(students, stcmp)
    tc.assertEqual(mybinsearch(sortedstudents, 3.5, stbincmp), 2)
    tc.assertEqual(mybinsearch(sortedstudents, 3.7, stbincmp), -1)


#################################################################################
# EXERCISE 2
#################################################################################
class PrefixSearcher():

    def __init__(self, document, k):  # creating and sorting prefixes

        self.doc = document
        self.k = k

    def search(self,
               q):  # Return true if the document contains search string q of length n - if q is longer than n, then raise an exception
        if len(q) > self.k:
            raise Exception("The string you are searching for is too long")
        else:
            slices = []
        for x in range(len(self.doc) - len(q) + 1):
            slices.append(self.doc[x:x + len(q)])
        if q in slices:
            return True
        else:
            return False


# 30 Points
def test2():
    print("#" * 80 + "\nSearch for substrings up to length n")
    test2_1()
    test2_2()


# 15Points
def test2_1():
    print("\t-search in hello world")
    tc = unittest.TestCase()
    p = PrefixSearcher("Hello World!", 1)
    tc.assertTrue(p.search("l"))
    tc.assertTrue(p.search("e"))
    tc.assertFalse(p.search("h"))
    tc.assertFalse(p.search("Z"))
    tc.assertFalse(p.search("Y"))
    p = PrefixSearcher("Hello World!", 2)
    tc.assertTrue(p.search("l"))
    tc.assertTrue(p.search("ll"))
    tc.assertFalse(p.search("lW"))


# 20 Points
def test2_2():
    print("\t-search in Moby Dick")
    tc = unittest.TestCase()
    md_url = 'https://www.gutenberg.org/files/2701/2701-0.txt'
    md_text = urllib.request.urlopen(md_url).read().decode()
    p = PrefixSearcher(md_text[0:1000], 4)
    tc.assertTrue(p.search("Moby"))
    tc.assertTrue(p.search("Dick"))


#################################################################################
# EXERCISE 3
#################################################################################
class SuffixArray():

    def __init__(self, document: str):  # creates a suffix array for document (a string).

        self.doc = document
        suffixes = [document[x:] for x in range(len(document))]
        sortedSuffixes = mysort(suffixes, intcmp)
        self.suffArray = [suffixes.index(sortedSuffixes[x]) for x in range(len(suffixes))]
        self.sortedSuffixes = sortedSuffixes

    def positions(self,
                  searchstr: str):  # Returns all positions of searchstr in the documented indexed by suffix array.

        x = 0
        while searchstr > self.sortedSuffixes[x]: x += 1  # now searchriting is between indixes x-1 and x
        pos = []
        while x < len(self.sortedSuffixes):
            if self.sortedSuffixes[x][:len(searchstr)] == searchstr:
                pos.append(self.suffArray[x])
                x += 1
            else:
                break
        return mysort(pos, intcmp)

    def contains(self, searchstr: str):  # returns True if searchstr is contained in document
        if len(self.positions(searchstr)) > 0:
            return True
        else:
            return False


# 40 Points
def test3():
    """Test suffix arrays."""
    print(80 * "#" + "\nTest suffix arrays.")
    test3_1()
    test3_2()


# 20 Points
def test3_1():
    print("\t-suffixarray on Hello World!")
    tc = unittest.TestCase()
    s = SuffixArray("Hello World!")
    tc.assertTrue(s.contains("l"))
    tc.assertTrue(s.contains("e"))
    tc.assertFalse(s.contains("h"))
    tc.assertFalse(s.contains("Z"))
    tc.assertFalse(s.contains("Y"))
    tc.assertTrue(s.contains("ello Wo"))


# 20 Points
def test3_2():
    print("\t-suffixarray on Moby Dick!")
    tc = unittest.TestCase()
    md_url = 'https://www.gutenberg.org/files/2701/2701-0.txt'
    md_text = urllib.request.urlopen(md_url).read().decode()
    s = SuffixArray(md_text[0:1000])
    tc.assertTrue(s.contains("Moby Dick"))
    tc.assertTrue(s.contains("Herman Melville"))
    tc.assertEqual(s.positions("Moby Dick"), [427])


#################################################################################
# TEST CASES
#################################################################################
def main():
    test1()
    test2()
    test3()


if __name__ == '__main__':
    main()
