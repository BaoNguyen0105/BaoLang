.source Lambda6.java
.class public Lambda6
.super java/lang/Object
.implements baolang/LambdaInterface
.field fact Ljava/lang/Object;

.method public <init>()V
Label0:
.var 0 is this Ljava/lang/Object; from Label0 to Label1
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	aload_0
	putfield Lambda6/fact Ljava/lang/Object;
	return
Label1:
.limit stack 3
.limit locals 1
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
.var 2 is n Ljava/lang/Object; from Label0 to Label1
	astore_2
	aload_2
	iconst_1
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	invokestatic baolang/BaoLangOperators/le(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
	checkcast java/lang/Boolean
	invokevirtual java/lang/Boolean/booleanValue()Z
	ifeq Label2
	iconst_1
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	goto Label3
Label2:
	aload_2
	aload_0
	getfield Lambda6/fact Ljava/lang/Object;
	new java/util/ArrayList
	dup
	invokespecial java/util/ArrayList/<init>()V
	dup
	aload_2
	iconst_1
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	invokestatic baolang/BaoLangOperators/sub(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
	invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
	pop
	invokeinterface baolang/LambdaInterface/call(Ljava/util/ArrayList;)Ljava/lang/Object; 2
	invokestatic baolang/BaoLangOperators/mul(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
Label3:
	nop
	areturn
Label1:
.limit stack 18
.limit locals 3
.end method
