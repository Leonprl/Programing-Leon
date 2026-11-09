# Exo 2 - ABCD Records

## Use case diagram

(mermaid has no real use case diagram so I used a flowchart: rounded boxes = use cases)

```mermaid
flowchart LR
    M([Member])
    N([Non-Member])
    OC([Order Processing Clerk])
    CC([Collection Department Clerk])

    subgraph ABCD Records system
        PO(Place Order)
        VM(Verify Membership)
        VA(Verify Item Availability)
        AD(Apply Discount)
        OU(Order Unavailable Items)
        PR(Process Order)
        PI(Print Invoice)
        PS(Print Shipping List)
        MP(Make Payment)
        SA(Send Membership Application)
    end

    M --- PO
    M --- MP
    N --- PO
    OC --- PR
    CC --- MP

    PO -. include .-> VM
    PO -. include .-> VA
    PR -. include .-> PI
    PR -. include .-> PS
    AD -. extend .-> PO
    OU -. extend .-> PO
    SA -. extend .-> VM
```

- `Verify Membership` and `Verify Item Availability` always happen when an order is placed -> include
- `Apply Discount` and `Order Unavailable Items` only for Royal members -> extend
- `Send Membership Application` only when the membership check fails (non-member) -> extend

## Class diagram

```mermaid
classDiagram
    class Member {
        <<abstract>>
        -int memberId
        -str name
        -str address
        +placeOrder(items) Order
        +pay(payment)
    }
    class RoyalMember {
        -float discountRate
        +orderUnavailable(item)
    }
    class RegularMember
    class NonMember {
        -str name
        -str address
        +requestMembership() MembershipApplication
    }
    class MembershipApplication {
        -date sentOn
        -str status
    }
    class Order {
        -int orderId
        -date date
        -str status
        +total() float
        +addLine(item, qty)
    }
    class OrderLine {
        -int quantity
        -bool backOrdered
        +subtotal() float
    }
    class Item {
        <<abstract>>
        -str title
        -str artist
        -float price
        -int stock
        +isAvailable() bool
    }
    class CD
    class Tape
    class Invoice {
        -int number
        -float amount
        +print()
    }
    class ShippingList {
        -str address
        +print()
    }
    class Payment {
        <<abstract>>
        -float amount
        -date date
        +process()* bool
    }
    class Cash
    class Check {
        -str checkNumber
    }
    class BankDraft {
        -str bank
    }
    class OrderProcessingClerk {
        -int employeeId
        +verifyMembership(member) bool
        +processOrder(order)
        +saveToDailyRecords(order)
    }
    class CollectionDepartmentClerk {
        -int employeeId
        +collectPayment(payment) bool
    }

    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft

    Member "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderLine
    OrderLine "0..*" --> "1" Item
    Order "1" *-- "1" Invoice
    Order "1" *-- "1" ShippingList
    Order "1" --> "0..*" Payment : paid by
    NonMember "1" --> "0..1" MembershipApplication : receives
    OrderProcessingClerk "1" --> "0..*" Order : processes
    CollectionDepartmentClerk "1" --> "0..*" Payment : handles
```

## Sequence diagram - Royal member orders 2 CDs (one unavailable), pays by check

```mermaid
sequenceDiagram
    actor R as RoyalMember
    participant OC as OrderProcessingClerk
    participant O as Order
    participant CD1 as CD 1
    participant CD2 as CD 2
    actor CC as CollectionDeptClerk

    R->>OC: placeOrder([cd1, cd2])
    OC->>OC: verifyMembership(R)
    OC->>O: create(R)
    OC->>CD1: isAvailable()
    CD1-->>OC: true
    OC->>O: addLine(cd1, 1)
    OC->>CD2: isAvailable()
    CD2-->>OC: false
    Note over OC,O: Royal member -> allowed to order unavailable items
    OC->>O: addLine(cd2, 1, backOrdered=true)
    OC->>O: applyDiscount(royal rate)
    OC->>O: printInvoice() + printShippingList()
    OC->>OC: saveToDailyRecords(O)
    R->>CC: pay(Check)
    CC->>CC: collectPayment(check)
    CC-->>R: payment confirmed
```
