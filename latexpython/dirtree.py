# This module lists relevant classes for our directory arrangement

import re,random,os

def keygen():
   letters_and_numbers = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
   digits = []
   for i in range(20):
      digits.append(random.choice(letters_and_numbers))
   key = ''.join(digits)
   return key

class Node:
   def __init__(self,val=None):
      self.val = val
      self.key = keygen()
      self.children = []
      self.parent = None

class DirTree:
   def __init__(self,root=None):
      self.root = root

   # Utility methods
   def insert(self,node,parent_key,rel_root):
      if self.root is None:
         self.root = node
      if rel_root.children == []:
         if parent_key != rel_root.key:
            return
         else:
            node.parent = rel_root
            rel_root.children.append(node)
      else:
         if parent_key == rel_root.key:
            node.parent = rel_root
            rel_root.children.append(node)
         else:
            for i in range(len(rel_root.children)):
               self.insert(node,parent_key,rel_root.children[i])

   def preorder_get_value(self,rel_root):
      val_list = []
      if rel_root is not None:
         val_list.append(rel_root.val)
      if rel_root.children == []:
         return [rel_root.val]
      else:
         for i in range(len(rel_root.children)):
            val_list.extend(self.preorder_get_value(rel_root.children[i]))
         return val_list

   def ancestors(self,rel_root):
      if rel_root.parent is None:
         return []
      else:
         ancestry_list = self.ancestors(rel_root.parent)
         ancestry_list.append(rel_root.parent.val)
         return ancestry_list

   def get_node_relations(self,rel_root):
      node_relations = []
      if rel_root is not None:
         node_relations.append((rel_root.val,rel_root.key,self.ancestors(rel_root),[rel_root.children[k].val for k in range(len(rel_root.children))]))
      if rel_root.children == []:
         return [(rel_root.val,rel_root.key,self.ancestors(rel_root),[])]
      else:
         for i in range(len(rel_root.children)):
            node_relations.extend(self.get_node_relations(rel_root.children[i]))
         return node_relations

def get_path_at_this_node(ancestry_list,current_node):
   if ancestry_list == []:
      prefix = ''
   else:
      prefix = ''
      for ancestors in ancestry_list:
         prefix = os.path.join(prefix,ancestors)
   path = os.path.join(prefix,current_node)
   return path

def buildtree(T):
   flag = True
   while flag:
      node_relations = T.get_node_relations(T.root)
      for node_tuples_set1 in node_relations:
         if node_tuples_set1[3] == []:
            path = get_path_at_this_node(node_tuples_set1[2],node_tuples_set1[0])
            if os.path.isdir(path):
               # Found a possible bug here: UNIX will sort the dir in this fashion: [1,10,11,2,...]
               # This needs fixing as we need strict ordering pattern for our documents
               dir_list = os.listdir(path)
               # Sort 'dir_list' and extract only relevant dir/files
               new_node_pattern = re.compile(r'^L\d+-(\d+)')
               tmp_list = [(dir_list[i],eval(new_node_pattern.search(dir_list[i]).group(1))) for i in range(len(dir_list)) if new_node_pattern.search(dir_list[i])]
               tmp_list = sorted(tmp_list,key=lambda x: x[1])
               dir_list = [tmp_list[i][0] for i in range(len(tmp_list))]
               for obj in dir_list:
                  if new_node_pattern.search(obj):
                     T.insert(Node(obj),node_tuples_set1[1],T.root)

      node_relations_after = T.get_node_relations(T.root)
      tex_extension_pattern = re.compile(r'\.tex$')
      leaf_nodes_tuples = []
      for node_tuples_set2 in node_relations_after:
         if node_tuples_set2[3] == []:
            leaf_nodes_tuples.append(node_tuples_set2)
      num_end_leaves = 0
      for leaf_tuples in leaf_nodes_tuples:
         if tex_extension_pattern.search(leaf_tuples[0]):
            num_end_leaves = num_end_leaves + 1

      if num_end_leaves != len(leaf_nodes_tuples):
         flag = True
      else:
         flag = False

   return T
