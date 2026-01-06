.source Lambda5.java
.class public Lambda5
.super java/lang/Object
.implements baolang/LambdaInterface
.field x Ljava/lang/Object;
.field y Ljava/lang/Object;

.method public <init>(Ljava/lang/Object;Ljava/lang/Object;)V
Label0:
.var 0 is this Ljava/lang/Object; from Label0 to Label1
	aload_0
	invokespecial java/lang/Object/<init>()V
.var 1 is x Ljava/lang/Object; from Label0 to Label1
	aload_0
	aload_1
	putfield Lambda5/x Ljava/lang/Object;
.var 2 is y Ljava/lang/Object; from Label0 to Label1
	aload_0
	aload_2
	putfield Lambda5/y Ljava/lang/Object;
	return
Label1:
.limit stack 5
.limit locals 3
.end method

.method public call(Ljava/util/ArrayList;)Ljava/lang/Object;
Label0:
.var 0 is this Ljava/lang/Object; from Label0 to Label1
.var 1 is args Ljava/lang/Object; from Label0 to Label1
	aload_1
	iconst_0
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	checkcast java/lang/Integer
	invokevirtual java/lang/Integer/intValue()I
	invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
.var 2 is z Ljava/lang/Object; from Label0 to Label1
	astore_2
	aload_0
	getfield Lambda5/x Ljava/lang/Object;
	aload_0
	getfield Lambda5/y Ljava/lang/Object;
	invokestatic baolang/BaoLangOperators/add(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
	aload_2
	invokestatic baolang/BaoLangOperators/add(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
	areturn
Label1:
.limit stack 10
.limit locals 3
.end method
