%define section free
%define gcj_support 1

%define manual  0

Name:           bcel
Version:        5.2
Release:        %mkrel 1.2
Epoch:          0
Summary:        Byte Code Engineering Library
License:        Apache License
Source0:        http://www.apache.org/dist/jakarta/bcel/source/bcel-5.2-src.tar.gz
URL:            http://jakarta.apache.org/%{name}/
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Requires:       regexp
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  regexp
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Byte Code Engineering Library (formerly known as JavaClass) is
intended to give users a convenient possibility to analyze, create, and
manipulate (binary) Java class files (those ending with .class). Classes
are represented by objects which contain all the symbolic information of
the given class: methods, fields and byte code instructions, in
particular.  Such objects can be read from an existing file, be
transformed by a program (e.g. a class loader at run-time) and dumped to
a file again. An even more interesting application is the creation of
classes from scratch at run-time. The Byte Code Engineering Library
(BCEL) may be also useful if you want to learn about the Java Virtual
Machine (JVM) and the format of Java .class files.  BCEL is already
being used successfully in several projects such as compilers,
optimizers, obsfuscators and analysis tools, the most popular probably
being the Xalan XSLT processor at Apache.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%if %manual
%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
Documentation for %{name}.
%endif

%prep
%setup -q

%build
export CLASSPATH=%(build-classpath regexp)
export OPT_JAR_LIST="ant/ant-nodeps"
%{ant} -Dbuild.dest=./build -Dbuild.dir=./build -Dname=%{name} compile jar javadoc

%install
%{__rm} -rf %{buildroot}
# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__install} -m 644 target/bcel-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__rm} -rf docs/api

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
%{__rm} -f %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt 
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%if %manual
%files manual
%defattr(0644,root,root,0755)
%doc docs/*
%endif

